import React from 'react';
import { List, ListItem, ListItemText, Paper } from '@mui/material';

const AlertsList = ({ alerts }) => {
  return (
    <Paper>
      <List>
        {alerts.map(alert => (
          <ListItem key={alert.id}>
            <ListItemText primary={alert.message} secondary={alert.timestamp} />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default AlertsList;
