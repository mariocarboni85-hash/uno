import React, { useState } from 'react';
import DistributedJobs from './DistributedJobs';
import GraphicWebProject from './GraphicWebProject';
import SystemAgent from './SystemAgent';
import ChatSuperAgent from './ChatSuperAgent';
import Watchdog from './Watchdog';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (res.ok && data.access_token) {
        onLogin(data.access_token);
      } else {
        setError(data.msg || 'Login fallito');
      }
    } catch (err) {
      setError('Errore di connessione');
    }
  };

  return (
    <div style={{display:'flex',flexDirection:'column',alignItems:'center',marginTop:'60px'}}>
      <button onClick={handleSubmit} style={{background:'none',border:'none',cursor:'pointer'}}>
        <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="40" cy="40" r="38" stroke="#0078D7" strokeWidth="4" fill="#F3F3F3" />
          <text x="50%" y="54%" textAnchor="middle" fontSize="32" fill="#0078D7" fontFamily="Arial" dy=".3em">SA</text>
        </svg>
      </button>
      <h2>Login Super Agent</h2>
      <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} style={{margin:'8px'}} />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} style={{margin:'8px'}} />
      <button type="submit" style={{margin:'8px',padding:'8px 24px',background:'#0078D7',color:'#fff',border:'none',borderRadius:'6px',fontWeight:'bold'}}>Login</button>
      {error && <p style={{color:'red'}}>{error}</p>}
    </div>
  );
}

function App() {
  const [token, setToken] = useState(null);
  const [page, setPage] = useState('dashboard');

  if (!token) {
    return <Login onLogin={setToken} />;
  }
  return (
    <div>
      <h1>Super Agent Dashboard</h1>
      <nav>
        <button onClick={() => setPage('dashboard')}>Dashboard</button>
        <button onClick={() => setPage('jobs')}>Job Distribuiti</button>
        <button onClick={() => setPage('graphicweb')}>Progetto Grafico/Web</button>
        <button onClick={() => setPage('systemagent')}>Gestione Sistema</button>
        <button onClick={() => setPage('chat')}>Chat Super Agent</button>
        <button onClick={() => setPage('watchdog')}>Watchdog Spesa</button>
        <button onClick={() => setToken(null)}>Logout</button>
      </nav>
      {page === 'dashboard' && (
        <div>
          <p>Benvenuto! Seleziona una sezione dal menu.</p>
        </div>
      )}
      {page === 'jobs' && <DistributedJobs token={token} />}
      {page === 'graphicweb' && <GraphicWebProject token={token} />}
      {page === 'systemagent' && <SystemAgent token={token} />}
      {page === 'chat' && <ChatSuperAgent token={token} />}
      {page === 'watchdog' && <Watchdog token={token} />}
    </div>
  );
}

export default App;
