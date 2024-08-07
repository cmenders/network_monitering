import React, { useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const HostnameCountsTable = ({ hostnameCounts }) => {
  useEffect(() => {
    console.log('HostnameCountsTable received hostnameCounts:', hostnameCounts);
  }, [hostnameCounts]);

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Hostname</TableCell>
            <TableCell>Count</TableCell>
            <TableCell>Latest Timestamp</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {hostnameCounts.map((hostnameCount, index) => (
            <TableRow key={index}>
              <TableCell>{hostnameCount.hostname}</TableCell>
              <TableCell>{hostnameCount.count}</TableCell>
              <TableCell>{hostnameCount.latest_timestamp}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default HostnameCountsTable;