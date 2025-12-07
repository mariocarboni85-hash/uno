import React, { useState } from 'react';
import axios from 'axios';
import { Button, TextField, Select, MenuItem, Typography, Box, List, ListItem, ListItemText } from '@mui/material';

function SystemAgent({ token }) {
  const [apps, setApps] = useState([]);
  const [processes, setProcesses] = useState([]);
  const [selectedApp, setSelectedApp] = useState('');
  const [log, setLog] = useState([]);
  const [authApp, setAuthApp] = useState('');
  const [authAllow, setAuthAllow] = useState(true);
  const [error, setError] = useState('');

  // Scansione applicazioni
  const scanApps = async () => {
    setError('');
    try {
      const res = await axios.get('http://localhost:5000/api/scan_apps', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setApps(res.data.apps);
    } catch (err) {
      setError('Errore scansione applicazioni');
    }
  };

  // Avvia applicazione
  const startApp = async () => {
    setError('');
    try {
      await axios.post('http://localhost:5000/api/start_app', { path: selectedApp }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLog(l => [...l, `Avviata: ${selectedApp}`]);
    } catch (err) {
      setError('Errore avvio applicazione');
    }
  };

  // Lista processi
  const listProcesses = async () => {
    setError('');
    try {
      const res = await axios.get('http://localhost:5000/api/list_processes', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProcesses(res.data.processes);
    } catch (err) {
      setError('Errore caricamento processi');
    }
  };

  // Chiudi processo
  const killProcess = async (pid) => {
    setError('');
    try {
      await axios.post('http://localhost:5000/api/kill_app', { pid }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLog(l => [...l, `Terminato PID: ${pid}`]);
      listProcesses();
    } catch (err) {
      setError('Errore terminazione processo');
    }
  };

  // Log azione
  const logAction = async (action, result) => {
    await axios.post('http://localhost:5000/api/log_action', { action, result }, {
      headers: { Authorization: `Bearer ${token}` }
    });
  };

  // Autorizzazione app
  const authorizeApp = async () => {
    setError('');
    try {
      await axios.post('http://localhost:5000/api/authorize', { app: authApp, allow: authAllow }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLog(l => [...l, `Autorizzazione: ${authApp} -> ${authAllow}`]);
    } catch (err) {
      setError('Errore autorizzazione');
    }
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5">Gestione Applicazioni e Processi</Typography>
      <Button variant="contained" onClick={scanApps} sx={{ m: 1 }}>Scansiona Applicazioni</Button>
      <List sx={{ maxHeight: 200, overflow: 'auto', border: '1px solid #ccc' }}>
        {apps.map((app, idx) => (
          <ListItem key={idx} button onClick={() => setSelectedApp(app)} selected={selectedApp === app}>
            <ListItemText primary={app} />
          </ListItem>
        ))}
      </List>
      <Button variant="contained" onClick={startApp} disabled={!selectedApp} sx={{ m: 1 }}>Avvia Applicazione</Button>
      <Typography variant="h6" sx={{ mt: 2 }}>Processi Attivi</Typography>
      <Button variant="outlined" onClick={listProcesses} sx={{ m: 1 }}>Aggiorna Lista Processi</Button>
      <List sx={{ maxHeight: 200, overflow: 'auto', border: '1px solid #ccc' }}>
        {processes.map((proc, idx) => (
          <ListItem key={idx}>
            <ListItemText primary={`${proc.name} (PID: ${proc.pid})`} />
            <Button color="error" onClick={() => killProcess(proc.pid)}>Termina</Button>
          </ListItem>
        ))}
      </List>
      <Typography variant="h6" sx={{ mt: 2 }}>Gestione Autorizzazioni</Typography>
      <TextField label="App" value={authApp} onChange={e => setAuthApp(e.target.value)} sx={{ m: 1 }} />
      <Select value={authAllow} onChange={e => setAuthAllow(e.target.value === 'true')} sx={{ m: 1 }}>
        <MenuItem value={true}>Consenti</MenuItem>
        <MenuItem value={false}>Blocca</MenuItem>
      </Select>
      <Button variant="contained" onClick={authorizeApp} sx={{ m: 1 }}>Aggiorna Autorizzazione</Button>
      <Typography variant="h6" sx={{ mt: 2 }}>Log Azioni</Typography>
      <List sx={{ maxHeight: 150, overflow: 'auto', border: '1px solid #ccc' }}>
        {log.map((entry, idx) => (
          <ListItem key={idx}><ListItemText primary={entry} /></ListItem>
        ))}
      </List>
      {error && <Typography color="error">{error}</Typography>}
    </Box>
  );
}

export default SystemAgent;
