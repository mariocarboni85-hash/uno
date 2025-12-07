import React, { useState } from 'react';

function GraphicWebProject({ token }) {
  const [nome, setNome] = useState('App Creativa');
  const [descrizione, setDescrizione] = useState('Un progetto grafico e web completo');
  const [tipo, setTipo] = useState('webapp');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await fetch('http://localhost:5000/api/graphic_web_project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ nome, descrizione, tipo })
      });
      const data = await res.json();
      if (res.ok) {
        setResult(data);
      } else {
        setError(data.msg || 'Errore nella creazione del progetto');
      }
    } catch (err) {
      setError('Errore di connessione');
    }
  };

  return (
    <div>
      <h2>Crea Progetto Grafico/Web</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Nome progetto" value={nome} onChange={e => setNome(e.target.value)} />
        <input type="text" placeholder="Descrizione" value={descrizione} onChange={e => setDescrizione(e.target.value)} />
        <select value={tipo} onChange={e => setTipo(e.target.value)}>
          <option value="webapp">WebApp</option>
          <option value="sito">Sito Internet</option>
          <option value="app_mobile">App Mobile</option>
        </select>
        <button type="submit">Crea progetto</button>
      </form>
      {error && <p style={{color:'red'}}>{error}</p>}
      {result && (
        <div>
          <h3>Progetto Creato</h3>
          <p><b>Nome:</b> {result.nome}</p>
          <p><b>Descrizione:</b> {result.descrizione}</p>
          <p><b>Tipo:</b> {result.tipo}</p>
          <h4>Team:</h4>
          <ul>
            {result.team.map((m, idx) => <li key={idx}>{m}</li>)}
          </ul>
          <h4>Log:</h4>
          <ul>
            {result.log.map((entry, idx) => <li key={idx}>{entry}</li>)}
          </ul>
          <p><b>Stato:</b> {result.stato}</p>
        </div>
      )}
    </div>
  );
}

export default GraphicWebProject;
