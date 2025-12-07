import React, { useState } from 'react';
import { Box, TextField, Button, Typography, List, ListItem, ListItemText, Paper } from '@mui/material';
import axios from 'axios';

function ChatSuperAgent({ token }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [error, setError] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;
    setError('');
    setMessages(msgs => [...msgs, { role: 'user', content: input }]);
    try {
      const res = await axios.post('http://localhost:5000/api/chat_superagent', { message: input }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessages(msgs => [...msgs, { role: 'agent', content: res.data.response }]);
      setInput('');
    } catch (err) {
      setError('Errore nella comunicazione con Super Agent');
    }
  };

  return (
    <Box sx={{ p: 2, maxWidth: 600, margin: 'auto' }}>
      <Typography variant="h5" sx={{ mb: 2 }}>Chat con Super Agent</Typography>
      <Paper sx={{ maxHeight: 300, overflow: 'auto', mb: 2, p: 1 }}>
        <List>
          {messages.map((msg, idx) => (
            <ListItem key={idx} alignItems="flex-start">
              <ListItemText primary={msg.role === 'user' ? 'Tu:' : 'Super Agent:'} secondary={msg.content} />
            </ListItem>
          ))}
        </List>
      </Paper>
      <TextField
        fullWidth
        label="Scrivi un messaggio"
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' ? sendMessage() : null}
        sx={{ mb: 2 }}
      />
      <Button variant="contained" onClick={sendMessage}>Invia</Button>
      {error && <Typography color="error" sx={{ mt: 2 }}>{error}</Typography>}
    </Box>
  );
}

export default ChatSuperAgent;
