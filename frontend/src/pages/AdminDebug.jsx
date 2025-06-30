import React, { useEffect, useState } from 'react';
import api from '../api';

function AdminDebug() {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const { data } = await api.get('/admin/debug');
        setStatus(data);
      } catch (err) {
        console.error('Failed to fetch debug status', err);
        setError('Failed to fetch status');
      }
    };
    fetchStatus();
  }, []);

  if (error) {
    return <div><h3>Debug Status</h3><p>{error}</p></div>;
  }

  if (!status) {
    return <div><h3>Debug Status</h3><p>Loading...</p></div>;
  }

  return (
    <div>
      <h3>Debug Status</h3>
      <ul>
        {Object.entries(status).map(([key, value]) => (
          <li key={key}>{key}: {String(value)}</li>
        ))}
      </ul>
    </div>
  );
}

export default AdminDebug;
