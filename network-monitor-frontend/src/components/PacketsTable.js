// src/components/PacketsTable.js
import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const PacketsTable = ({ packets }) => {
  console.log('PacketsTable received packets:', packets);  // Log packets to verify data is passed

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Timestamp</TableCell>
            <TableCell>Source IP</TableCell>
            <TableCell>Destination IP</TableCell>
            <TableCell>Protocol</TableCell>
            <TableCell>Source Port</TableCell>
            <TableCell>Destination Port</TableCell>
            <TableCell>Details</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {packets.map((packet, index) => (
            <TableRow key={index}>
              <TableCell>{packet.timestamp}</TableCell>
              <TableCell>{packet.src_ip}</TableCell>
              <TableCell>{packet.dst_ip}</TableCell>
              <TableCell>{packet.protocol}</TableCell>
              <TableCell>{packet.src_port}</TableCell>
              <TableCell>{packet.dst_port}</TableCell>
              <TableCell>{packet.details}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default PacketsTable;