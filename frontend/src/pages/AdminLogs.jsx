import React, { useEffect, useState } from 'react';
import api from '../api';

function AdminLogs({ token }) {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const { data } = await api.get('/admin/logs');
        setLogs(data);
      } catch (err) {
        console.error("Failed to fetch logs", err);
      }
    };
    fetchLogs();
  }, []);

  return (
    <div>
      <h3>Admin Logs</h3>
      <ul>
        {logs.map((log) => (
          <li key={log.id}>{log.event}: {log.detail}</li>
        ))}
      </ul>
    </div>
  );
}

export default AdminLogs;
