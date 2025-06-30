import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api, { setToken } from '../api';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const params = new URLSearchParams({ username, password });
      const { data } = await api.post('/token', params);
      setToken(data.access_token);
      const meRes = await api.get('/me');
      onLogin(data.access_token, meRes.data);
      navigate('/');
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setError(detail ? `Login failed: ${detail}` : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {error && <p>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
}

export default Login;
