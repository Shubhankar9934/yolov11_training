import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress, Button } from '@mui/material';
import axios from 'axios';

const MetricCard = ({ label, value }) => (
  <Box sx={{
    p: 2,
    border: '1px solid #ddd',
    borderRadius: 1,
    textAlign: 'center'
  }}>
    <Typography variant="subtitle2" color="text.secondary">
      {label}
    </Typography>
    <Typography variant="h6">
      {value}
    </Typography>
  </Box>
);

function TrainingStatus({ status }) {
  const [trainingStatus, setTrainingStatus] = useState(status);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);
  const [device, setDevice] = useState('Checking...');
  const [metrics, setMetrics] = useState({
    precision: 0,
    recall: 0,
    mAP50: 0,
    mAP50_95: 0
  });
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (status === 'training') {
      const interval = setInterval(async () => {
        try {
          const response = await axios.get('/api/training-status');
          setTrainingStatus(response.data.status);
          setProgress(response.data.progress);
          setDevice(response.data.device);

          // Update metrics if available
          if (response.data.metrics) {
            setMetrics({
              precision: response.data.metrics.precision || 0,
              recall: response.data.metrics.recall || 0,
              mAP50: response.data.metrics.mAP50 || 0,
              mAP50_95: response.data.metrics.mAP50_95 || 0
            });
          }

          // Update training history
          if (response.data.history) {
            setHistory(prev => [
              ...prev,
              {
                timestamp: new Date().toISOString(),
                metrics: response.data.metrics || {},
                progress: response.data.progress
              }
            ]);
          }
          
          if (response.data.status === 'completed') {
            clearInterval(interval);
          }
        } catch (err) {
          setError(err.response?.data?.error || 'Failed to fetch training status');
          console.error('Status fetch error:', err);
          clearInterval(interval);
        }
      }, 5000);

      return () => clearInterval(interval);
    }
  }, [status]);

  const handleDownload = () => {
    window.location.href = '/api/download-trained-model';
  };

  return (
    <Box sx={{ 
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      mt: 4
    }}>
      <Typography variant="h5" gutterBottom>
        Training Status
      </Typography>

      {trainingStatus === 'training' && (
        <>
          <CircularProgress
            variant="determinate"
            value={progress}
            size={80}
            thickness={5}
            sx={{ mb: 2 }}
          />
          <Typography variant="body1">
            Progress: {progress}%
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Using: {device}
          </Typography>

          <Box sx={{ mt: 4, width: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Training Metrics
            </Typography>
            <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 2 }}>
              <MetricCard label="Precision" value={metrics.precision.toFixed(2)} />
              <MetricCard label="Recall" value={metrics.recall.toFixed(2)} />
              <MetricCard label="mAP@50" value={metrics.mAP50.toFixed(2)} />
              <MetricCard label="mAP@50-95" value={metrics.mAP50_95.toFixed(2)} />
            </Box>
          </Box>

          <Box sx={{ mt: 4, width: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Training History
            </Typography>
            <Box sx={{ maxHeight: 200, overflowY: 'auto' }}>
              {history.map((entry, index) => (
                <Box key={index} sx={{ mb: 1, p: 1, borderBottom: '1px solid #eee' }}>
                  <Typography variant="body2">
                    {new Date(entry.timestamp).toLocaleTimeString()}
                  </Typography>
                  <Typography variant="body2">
                    Progress: {entry.progress}% | Precision: {entry.metrics.precision?.toFixed(2) || 'N/A'}
                  </Typography>
                </Box>
              ))}
            </Box>
          </Box>
        </>
      )}

      {trainingStatus === 'completed' && (
        <>
          <Typography variant="body1" color="success.main" sx={{ mb: 2 }}>
            Training completed successfully!
          </Typography>
          <Button 
            variant="contained"
            color="success"
            onClick={handleDownload}
          >
            Download Trained Model
          </Button>
        </>
      )}

      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          Error: {error}
        </Typography>
      )}
    </Box>
  );
}

export default TrainingStatus;