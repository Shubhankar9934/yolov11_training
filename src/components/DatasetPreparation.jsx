import React, { useState } from 'react';
import { Stepper, Step, StepLabel, Button, Typography, Box } from '@mui/material';
import axios from 'axios';

const steps = [
  'Upload Dataset',
  'Split Dataset',
  'Count Files',
  'Check Labels',
  'Create data.yaml',
  'Train Model'
];

function DatasetPreparation({ onTrainingStart }) {
  const [activeStep, setActiveStep] = useState(0);
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [trainingId, setTrainingId] = useState(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    
    // Validate file
    if (!file) {
      setError('No file selected');
      return;
    }

    if (!file.name.endsWith('.zip')) {
      setError('Only .zip files are allowed');
      return;
    }

    if (file.size > 100 * 1024 * 1024) { // 100MB limit
      setError('File size must be less than 100MB');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setError(null);
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          console.log(`Upload progress: ${percentCompleted}%`);
        }
      });
      
      setFile(response.data);
      setActiveStep(1);
    } catch (err) {
      setError(err.response?.data?.error || 'File upload failed');
      console.error('Upload error:', err);
    }
  };

  const handleStep = async (operation) => {
    try {
      await axios.post('/api/prepare-dataset', { operation });
      setActiveStep(prev => prev + 1);
    } catch (err) {
      setError(`Error during ${operation}`);
    }
  };

  const startTraining = async () => {
    try {
      const response = await axios.post('/api/train');
      setTrainingId(response.data.id);
      onTrainingStart('training');
      setActiveStep(5);
    } catch (err) {
      setError('Training failed to start');
    }
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Stepper activeStep={activeStep} alternativeLabel>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      {activeStep === 0 && (
        <Box sx={{ mt: 4 }}>
          <input
            accept=".zip"
            style={{ display: 'none' }}
            id="dataset-upload"
            type="file"
            onChange={handleFileUpload}
          />
          <label htmlFor="dataset-upload">
            <Button variant="contained" component="span">
              Upload Dataset
            </Button>
          </label>
        </Box>
      )}

      {activeStep > 0 && activeStep < 5 && (
        <Box sx={{ mt: 4 }}>
          <Button 
            variant="contained"
            onClick={() => handleStep(steps[activeStep].toLowerCase())}
          >
            {steps[activeStep]}
          </Button>
        </Box>
      )}

      {activeStep === 5 && (
        <Box sx={{ mt: 4 }}>
          <Button 
            variant="contained"
            onClick={startTraining}
          >
            Start Training
          </Button>
        </Box>
      )}

      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          Error: {error}
        </Typography>
      )}
    </Box>
  );
}

export default DatasetPreparation;