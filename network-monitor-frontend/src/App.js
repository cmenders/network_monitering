import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Grid, Paper, Typography, Button } from '@mui/material';
import PacketsTable from './components/PacketsTable';
import AlertsList from './components/AlertsList';
import PacketHistogram from './components/PacketHistogram';

const App = () => {
  const [packets, setPackets] = useState([]);
  const [allPackets, setAllPackets] = useState([]); // For cumulative histogram
  const [alerts, setAlerts] = useState([]);
  const [captureStarted, setCaptureStarted] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [timer, setTimer] = useState(0);
  const [timerInterval, setTimerInterval] = useState(null);

  useEffect(() => {
    let socket;
    if (captureStarted) {
      const fetchInitialData = async () => {
        try {
          const packetsResult = await axios.get('http://127.0.0.1:8000/api/packets/');
          setPackets(packetsResult.data.slice(-10).sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)));  // Show only the latest 10 packets sorted by timestamp
          setAllPackets(packetsResult.data); // For cumulative histogram
          
          const alertsResult = await axios.get('http://127.0.0.1:8000/api/alerts/');
          setAlerts(alertsResult.data);
        } catch (error) {
          console.error('Error fetching initial data:', error);
        }
      };

      fetchInitialData();

      socket = new WebSocket('ws://127.0.0.1:8001/ws/packets/');

      socket.onopen = () => {
        console.log('Connected to WebSocket');
      };

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('WebSocket message received:', data);  // Log incoming data
        if (data.type === 'packet') {
          setPackets((prevPackets) => {
            const updatedPackets = [data.packet, ...prevPackets].slice(0, 10).sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
            return updatedPackets;  // Keep only the latest 10 packets sorted by timestamp
          });
          setAllPackets((prevPackets) => [data.packet, ...prevPackets]); // Cumulative histogram
        }
        if (data.type === 'alerts') {
          setAlerts(data.alerts);
        }
      };

      socket.onclose = (event) => {
        console.log('WebSocket connection closed', event);
      };

      const intervalId = setInterval(async () => {
        try {
          const result = await axios.get('http://127.0.0.1:8000/api/packets/');
          setPackets(result.data.slice(-10).sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)));  // Show only the latest 10 packets sorted by timestamp
          setAllPackets(result.data); // For cumulative histogram
        } catch (error) {
          console.error('Error fetching packets:', error);
        }
      }, 1000);

      // Update the timer every second
      const timerId = setInterval(() => {
        setTimer((prevTimer) => prevTimer + 1);
      }, 1000);
      setTimerInterval(timerId);

      return () => {
        socket.close();
        clearInterval(intervalId);
        clearInterval(timerId);
      };
    }
  }, [captureStarted]);

  const handleStartCapture = async () => {
    if (captureStarted) {
      try {
        await axios.get('http://127.0.0.1:8000/api/stop_capture/');
        setCaptureStarted(false);
        clearInterval(timerInterval); // Stop the timer
      } catch (error) {
        console.error('Error stopping capture:', error);
      }
    } else {
      try {
        await axios.get('http://127.0.0.1:8000/api/start_capture/');
        setCaptureStarted(true);
        setStartTime(Date.now());
        setTimer(0);
      } catch (error) {
        console.error('Error starting capture:', error);
      }
    }
  };

  return (
    <Container>
      <Typography variant="h2" gutterBottom>
        Network Monitor Dashboard
      </Typography>
      <Button variant="contained" color="primary" onClick={handleStartCapture}>
        {captureStarted ? 'Stop Capture' : 'Start Capture'}
      </Button>
      {startTime && (
        <Typography variant="h6" gutterBottom style={{ float: 'right' }}>
          Timer: {Math.floor(timer / 60)}:{(timer % 60).toString().padStart(2, '0')}
        </Typography>
      )}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper>
            <Typography variant="h4" gutterBottom>
              Captured Packets
            </Typography>
            <PacketsTable packets={packets} />
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper>
            <Typography variant="h4" gutterBottom>
              Packet Histogram
            </Typography>
            <PacketHistogram packets={allPackets} />
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper>
            <Typography variant="h4" gutterBottom>
              Alerts
            </Typography>
            <AlertsList alerts={alerts} />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default App;