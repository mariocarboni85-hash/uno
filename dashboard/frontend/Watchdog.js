import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Watchdog({ token }) {
  const [active, setActive] = useState(false);
  const [limit, setLimit] = useState(1000);
  const [blocked, setBlocked] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [amount, setAmount] = useState('');
  const [desc, setDesc] = useState('');
  const [msg, setMsg] = useState('');

  // Carica stato watchdog
  useEffect(() => {
    axios.get('http://localhost:5000/api/watchdog/status', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => {
      setActive(res.data.active);
      setLimit(res.data.limit);
      setBlocked(res.data.blocked);
    });
    axios.get('http://localhost:5000/api/watchdog/notifications', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setNotifications(res.data));
  }, [token, msg]);

  // Attiva/disattiva watchdog
  const toggleWatchdog = () => {
    const url = active ? '/api/watchdog/deactivate' : '/api/watchdog/activate';
    axios.post(`http://localhost:5000${url}`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    }).then(() => setMsg(active ? 'Disattivato' : 'Attivato'));
  };

  // Imposta soglia
  const handleLimit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5000/api/watchdog/set_limit', { limit: Number(limit) }, {
      headers: { Authorization: `Bearer ${token}` }
    }).then(() => setMsg('Soglia aggiornata'));
  };

  // Aggiungi movimento
  const handleMovement = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5000/api/watchdog/add_movement', { amount: Number(amount), desc }, {
      headers: { Authorization: `Bearer ${token}` }
    }).then(() => { setMsg('Movimento aggiunto'); setAmount(''); setDesc(''); });
  };

  return (
    <div>
      <h2>Watchdog Spesa</h2>
      <p>Stato: {active ? 'Attivo' : 'Disattivo'} | Soglia: {limit} | Blocco: {blocked ? 'ATTIVO' : 'Nessun blocco'}</p>
      <button onClick={toggleWatchdog}>{active ? 'Disattiva' : 'Attiva'} Watchdog</button>
      <form onSubmit={handleLimit}>
        <input type="number" value={limit} onChange={e => setLimit(e.target.value)} />
        <button type="submit">Imposta soglia</button>
      </form>
      <form onSubmit={handleMovement}>
        <input type="number" value={amount} onChange={e => setAmount(e.target.value)} placeholder="Importo" />
        <input type="text" value={desc} onChange={e => setDesc(e.target.value)} placeholder="Descrizione" />
        <button type="submit">Aggiungi movimento</button>
      </form>
      {msg && <p style={{color:'green'}}>{msg}</p>}
      <h3>Notifiche</h3>
      <ul>
        {notifications.map((n, idx) => (
          <li key={idx}><b>{n.type}</b>: {n.msg} <i>{n.date}</i></li>
        ))}
      </ul>
    </div>
  );
}

export default Watchdog;
