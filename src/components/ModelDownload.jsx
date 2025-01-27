import React from 'react';
import { Button, Typography } from '@mui/material';

function ModelDownload() {
  return (
    <div>
      <Typography variant="h6" gutterBottom>
        Model Download
      </Typography>
      <Button 
        variant="contained" 
        color="primary"
        onClick={() => window.location.href = '/api/download-trained-model'}
      >
        Download Trained Model
      </Button>
    </div>
  );
}

export default ModelDownload;