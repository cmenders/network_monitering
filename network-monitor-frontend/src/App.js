import './App.css';

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [packets, setPackets] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchPackets = async () => {
      const result = await axios.get('http://127.0.0.1:8000/api/packets/');
      setPackets(result.data);
    };

    const fetchAlerts = async () => {
      const result = await axios.get('http://127.0.0.1:8000/api/alerts/');
      setAlerts(result.data);
    };

    fetchPackets();
    fetchAlerts();
  }, []);

  return (
    <div>
      <h1>Network Monitor Dashboard</h1>
      <h2>Captured Packets</h2>
      <table>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Source IP</th>
            <th>Destination IP</th>
            <th>Protocol</th>
            <th>Source Port</th>
            <th>Destination Port</th>
            <th>Details</th>
          </tr>
        </thead>
        <tbody>
          {packets.map(packet => (
            <tr key={packet.id}>
              <td>{packet.timestamp}</td>
              <td>{packet.src_ip}</td>
              <td>{packet.dst_ip}</td>
              <td>{packet.protocol}</td>
              <td>{packet.src_port}</td>
              <td>{packet.dst_port}</td>
              <td>{packet.details}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Alerts</h2>
      <ul>
        {alerts.map(alert => (
          <li key={alert.id}>{alert.timestamp} - {alert.message}</li>
        ))}
      </ul>
    </div>
  );
};

export default App;
