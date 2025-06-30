import React, { useState } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Accounts from './pages/Accounts';
import AdminLogs from './pages/AdminLogs';
import AdminSettings from './pages/AdminSettings';
import AdminDebug from './pages/AdminDebug';
import Profile from './pages/Profile';
import Tutorial from './components/Tutorial';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [firstLogin, setFirstLogin] = useState(false);
  const [user, setUser] = useState(null);

  if (!token) {
    return <Login onLogin={(tok, user) => { setToken(tok); setUser(user); setFirstLogin(user.first_login); localStorage.setItem('token', tok); }} />;
  }
  if (firstLogin) {
    return <Tutorial onFinish={() => setFirstLogin(false)} />;
  }

  return (
    <Routes>
      <Route path="/" element={<Dashboard user={user} />} />
      <Route path="/accounts" element={<Accounts token={token} />} />
      <Route path="/profile" element={<Profile token={token} user={user} />} />
      <Route path="/admin/logs" element={user?.is_admin ? <AdminLogs token={token} /> : <Navigate to="/" />} />
      <Route path="/admin/settings" element={user?.is_admin ? <AdminSettings token={token} /> : <Navigate to="/" />} />
      <Route path="/admin/debug" element={user?.is_admin ? <AdminDebug token={token} /> : <Navigate to="/" />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

export default App;
