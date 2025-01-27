import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Container, CssBaseline, Box, ThemeProvider, createTheme } from '@mui/material';
import DatasetPreparation from './components/DatasetPreparation';
import TrainingStatus from './components/TrainingStatus';
import ModelDownload from './components/ModelDownload';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#9c27b0',
    },
  },
});

function App() {
  const [trainingStatus, setTrainingStatus] = useState(null);

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <CssBaseline />
        <Container maxWidth="lg">
          <Box sx={{ my: 4 }}>
            <Routes>
              <Route path="/" element={
                <DatasetPreparation
                  onTrainingStart={(status) => setTrainingStatus(status)}
                />
              } />
              <Route path="/status" element={
                <TrainingStatus
                  status={trainingStatus}
                />
              } />
              <Route path="/download" element={<ModelDownload />} />
            </Routes>
          </Box>
        </Container>
      </Router>
    </ThemeProvider>
  );
}

export default App;