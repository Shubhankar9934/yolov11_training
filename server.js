const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const { PythonShell } = require('python-shell');
const archiver = require('archiver');

const app = express();
const port = process.env.PORT || 5001;

// Database setup
const db = new sqlite3.Database('./yolov8_training.db', (err) => {
  if (err) {
    console.error('Database connection error:', err.message);
  } else {
    console.log('Connected to SQLite database');
    initializeDatabase();
  }
});

// Middleware
app.use(cors());
app.use(express.json());
app.use('/uploads', express.static(path.join(__dirname, 'public/uploads')));

// File upload configuration
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'public/uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname);
  }
});
const upload = multer({ storage });

// Initialize database tables
function initializeDatabase() {
  db.run(`CREATE TABLE IF NOT EXISTS uploaded_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending'
  )`);

  db.run(`CREATE TABLE IF NOT EXISTS training_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    status TEXT DEFAULT 'pending',
    device TEXT,
    metrics TEXT,
    history TEXT
  )`);
}

// API Routes
app.post('/api/upload', upload.single('file'), (req, res) => {
  const { filename, path } = req.file;
  
  db.run(
    'INSERT INTO uploaded_files (filename) VALUES (?)',
    [filename],
    function(err) {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json({
        id: this.lastID,
        filename,
        path
      });
    }
  );
});

app.post('/api/prepare-dataset', async (req, res) => {
  const { operation } = req.body;
  
  if (!operation) {
    return res.status(400).json({
      error: 'Operation is required',
      validOperations: ['split', 'count', 'check', 'create']
    });
  }

  const validOperations = {
    split: './scripts/split_dataset.py',
    count: './scripts/count_files.py',
    check: './scripts/check_labels.py',
    create: './scripts/create_data_yaml.py'
  };

  if (!validOperations[operation]) {
    return res.status(400).json({
      error: 'Invalid operation',
      validOperations: Object.keys(validOperations)
    });
  }

  try {
    // Validate script exists
    if (!fs.existsSync(validOperations[operation])) {
      return res.status(404).json({
        error: 'Script not found',
        scriptPath: validOperations[operation]
      });
    }

    PythonShell.run(validOperations[operation], null, (err, results) => {
      if (err) {
        console.error('PythonShell Error:', err);
        return res.status(500).json({
          error: 'Dataset preparation failed',
          details: err.message,
          stack: err.stack
        });
      }
      
      res.json({
        status: 'success',
        operation,
        results: results?.join('\n') || 'No output'
      });
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      error: 'Internal server error',
      details: error.message,
      stack: error.stack
    });
  }
});

app.get('/api/download-trained-model', (req, res) => {
  const modelPath = path.join(__dirname, 'runs/detect/train/weights/best.pt');
  
  if (!fs.existsSync(modelPath)) {
    return res.status(404).json({ error: 'Model not found' });
  }

  res.download(modelPath, 'best.pt');
});

app.get('/api/download-frames', (req, res) => {
  const framesDir = path.join(__dirname, 'public/uploads/extracted_frames');
  const output = fs.createWriteStream('frames.zip');
  const archive = archiver('zip', { zlib: { level: 9 } });

  output.on('close', () => {
    res.download('frames.zip', () => {
      fs.unlinkSync('frames.zip');
    });
  });

  archive.on('error', (err) => {
    res.status(500).json({ error: err.message });
  });

  archive.pipe(output);
  archive.directory(framesDir, false);
  archive.finalize();
});

// Training status endpoint
app.get('/api/training-status', (req, res) => {
  db.get(
    'SELECT * FROM training_tasks ORDER BY id DESC LIMIT 1',
    (err, row) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      
      if (!row) {
        return res.json({
          status: 'not_started',
          progress: 0,
          device: 'N/A',
          metrics: null,
          history: []
        });
      }

      // Calculate progress based on start and end times
      const progress = row.end_time
        ? 100
        : Math.floor(
            ((new Date() - new Date(row.start_time)) /
            (1000 * 60 * 60)) * 100
          );

      // Parse metrics from training log
      let metrics = {};
      try {
        if (row.metrics) {
          metrics = JSON.parse(row.metrics);
        }
      } catch (e) {
        console.error('Error parsing metrics:', e);
      }

      // Get training history
      db.all(
        'SELECT * FROM training_tasks WHERE id = ? ORDER BY start_time ASC',
        [row.id],
        (err, history) => {
          if (err) {
            console.error('Error fetching history:', err);
          }

          res.json({
            status: row.status,
            progress: Math.min(progress, 100),
            device: row.device || 'CPU',
            metrics,
            history: history.map(h => ({
              timestamp: h.start_time,
              metrics: h.metrics ? JSON.parse(h.metrics) : {},
              progress: Math.floor(
                ((new Date(h.start_time) - new Date(row.start_time)) /
                (1000 * 60 * 60)) * 100
              )
            }))
          });
        }
      );
    }
  );
});

// Start training endpoint
app.post('/api/train', (req, res) => {
  const options = {
    mode: 'text',
    pythonOptions: ['-u'], // unbuffered output
    scriptPath: './scripts',
    args: []
  };

  db.run(
    'INSERT INTO training_tasks (model_name, status) VALUES (?, ?)',
    ['yolov8', 'training'],
    function(err) {
      if (err) {
        return res.status(500).json({ error: err.message });
      }

      const trainingId = this.lastID;

      const pythonProcess = PythonShell.run('train_yolov8.py', options, (err, results) => {
        const status = err ? 'failed' : 'completed';
        
        db.run(
          'UPDATE training_tasks SET status = ?, end_time = CURRENT_TIMESTAMP WHERE id = ?',
          [status, trainingId],
          (updateErr) => {
            if (updateErr) {
              console.error('Error updating training status:', updateErr);
            }
          }
        );

        if (err) {
          return res.status(500).json({ error: err.message });
        }
        
        res.json({ id: trainingId });
      });

      // Handle real-time output from Python process
      pythonProcess.on('message', (message) => {
        if (message.startsWith('PROGRESS:')) {
          const progress = parseInt(message.split(':')[1]);
          db.run(
            'UPDATE training_tasks SET progress = ? WHERE id = ?',
            [progress, trainingId]
          );
        }
        else if (message.startsWith('DEVICE:')) {
          const device = message.split(':')[1];
          db.run(
            'UPDATE training_tasks SET device = ? WHERE id = ?',
            [device, trainingId]
          );
        }
        else if (message.startsWith('METRICS:')) {
          const metrics = message.split(':')[1];
          db.run(
            'UPDATE training_tasks SET metrics = ? WHERE id = ?',
            [metrics, trainingId]
          );
        }
      });
    }
  );
});

// Start server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
  console.log(`API available at http://localhost:${port}/api`);
});