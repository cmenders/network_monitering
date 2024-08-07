import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const AlertsList = ({ alerts }) => {
  const alertCounts = alerts.reduce((acc, alert) => {
    const key = alert.message;
    if (!acc[key]) {
      acc[key] = {
        message: alert.message,
        count: 0,
        timestamp: alert.timestamp
      };
    }
    acc[key].count += 1;
    acc[key].timestamp = alert.timestamp;
    return acc;
  }, {});

  const sortedAlerts = Object.values(alertCounts).sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Alert</TableCell>
            <TableCell>Count</TableCell>
            <TableCell>Latest Timestamp</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {sortedAlerts.map((alert, index) => (
            <TableRow key={index}>
              <TableCell>{alert.message}</TableCell>
              <TableCell>{alert.count}</TableCell>
              <TableCell>{alert.timestamp}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default AlertsList;