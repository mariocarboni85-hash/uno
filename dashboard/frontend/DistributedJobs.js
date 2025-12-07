import React, { useState, useEffect } from 'react';

function DistributedJobs({ token }) {
  const [jobs, setJobs] = useState([]);
  const [agentId, setAgentId] = useState('');
  const [config, setConfig] = useState('{}');
  const [error, setError] = useState('');
  const [selectedJob, setSelectedJob] = useState(null);
  const [jobDetail, setJobDetail] = useState(null);

  // Carica tutti i job
  useEffect(() => {
    fetch('http://localhost:5000/api/distributed_jobs', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(setJobs)
      .catch(() => setError('Errore nel caricamento job distribuiti'));
  }, [token, jobDetail]);

  // Crea nuovo job
  const handleCreateJob = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await fetch('http://localhost:5000/api/distributed_jobs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ agent_id: agentId, config: JSON.parse(config) })
      });
      const data = await res.json();
      if (res.ok && data.job_id) {
        setSelectedJob(data.job_id);
      } else {
        setError(data.msg || 'Creazione job fallita');
      }
    } catch (err) {
      setError('Errore di connessione o formato config non valido');
    }
  };

  // Carica dettagli job selezionato
  useEffect(() => {
    if (selectedJob) {
      fetch(`http://localhost:5000/api/distributed_jobs/${selectedJob}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(setJobDetail)
        .catch(() => setError('Errore nel caricamento dettagli job'));
    }
  }, [selectedJob, token]);

  return (
    <div>
      <h2>Job Distribuiti</h2>
      <form onSubmit={handleCreateJob}>
        <input type="text" placeholder="Agent ID" value={agentId} onChange={e => setAgentId(e.target.value)} />
        <input type="text" placeholder="Config JSON" value={config} onChange={e => setConfig(e.target.value)} />
        <button type="submit">Avvia Job Distribuito</button>
      </form>
      {error && <p style={{color:'red'}}>{error}</p>}
      <ul>
        {jobs.map(job => (
          <li key={job.id}>
            <button onClick={() => setSelectedJob(job.id)}>
              Job {job.id} - Agente {job.agent_id} - {job.status} - {job.progress}%
            </button>
          </li>
        ))}
      </ul>
      {jobDetail && (
        <div>
          <h3>Dettagli Job</h3>
          <p>ID: {jobDetail.id}</p>
          <p>Agente: {jobDetail.agent_id}</p>
          <p>Status: {jobDetail.status}</p>
          <p>Progresso: {jobDetail.progress}%</p>
          <h4>Log:</h4>
          <ul>
            {jobDetail.log.map((entry, idx) => <li key={idx}>{entry}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}

export default DistributedJobs;
