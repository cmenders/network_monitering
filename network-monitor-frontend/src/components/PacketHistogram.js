import React from 'react';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

const PacketHistogram = ({ packets }) => {
  const portCounts = packets.reduce((acc, packet) => {
    const port = packet.dst_port || 'unknown';
    acc[port] = (acc[port] || 0) + 1;
    return acc;
  }, {});

  const data = {
    labels: Object.keys(portCounts),
    datasets: [
      {
        label: 'Packet Count',
        data: Object.values(portCounts),
        backgroundColor: 'rgba(75,192,192,0.6)',
      },
    ],
  };

  return <Bar data={data} />;
};

export default PacketHistogram;
