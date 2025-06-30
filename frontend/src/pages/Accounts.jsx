import React, { useState, useEffect } from 'react';
import api from '../api';

function Accounts({ token }) {
  const [amazonStatus, setAmazonStatus] = useState(null);
  const [epicStatus, setEpicStatus] = useState(null);
  const [gogStatus, setGogStatus] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const { data: amazon } = await api.get('/accounts/amazon/status');
        setAmazonStatus(amazon);
      } catch (err) {
        console.error("Failed to fetch Amazon status", err);
      }
      try {
        const { data: epic } = await api.get('/accounts/epic/status');
        setEpicStatus(epic);
      } catch (err) {
        console.error("Failed to fetch Epic status", err);
      }
      try {
        const { data: gog } = await api.get('/accounts/gog/status');
        setGogStatus(gog);
      } catch (err) {
        console.error("Failed to fetch GOG status", err);
      }
    };
    fetchStatus();
  }, []);

  const handleAmazonLogin = async () => {
    try {
      await api.post('/accounts/amazon/login');
      setAmazonStatus({ logged_in: true });
    } catch (err) {
      console.error("Amazon login failed", err);
    }
  };

  const handleAmazonLogout = async () => {
    try {
      await api.delete('/accounts/amazon/logout');
      setAmazonStatus({ logged_in: false });
    } catch (err) {
      console.error("Amazon logout failed", err);
    }
  };

  const handleEpicLogin = async () => {
    try {
      await api.post('/accounts/epic/login');
      setEpicStatus({ logged_in: true });
    } catch (err) {
      console.error("Epic login failed", err);
    }
  };

  const handleEpicLogout = async () => {
    try {
      await api.delete('/accounts/epic/logout');
      setEpicStatus({ logged_in: false });
    } catch (err) {
      console.error("Epic logout failed", err);
    }
  };

  const handleGogLogin = async () => {
    try {
      await api.post('/accounts/gog/login');
      setGogStatus({ logged_in: true });
    } catch (err) {
      console.error("GOG login failed", err);
    }
  };

  const handleGogLogout = async () => {
    try {
      await api.delete('/accounts/gog/logout');
      setGogStatus({ logged_in: false });
    } catch (err) {
      console.error("GOG logout failed", err);
    }
  };

  return (
    <div>
      <h3>Amazon Account</h3>
      {amazonStatus && amazonStatus.logged_in ? (
        <div>
          <p>Logged in to Amazon</p>
          <button onClick={handleAmazonLogout}>Logout</button>
        </div>
      ) : (
        <div>
          <p>Not logged in</p>
          <button onClick={handleAmazonLogin}>Login</button>
        </div>
      )}

      <h3>Epic Games</h3>
      {epicStatus && epicStatus.logged_in ? (
        <div>
          <p>Logged in to Epic</p>
          <button onClick={handleEpicLogout}>Logout</button>
        </div>
      ) : (
        <div>
          <p>Not logged in</p>
          <button onClick={handleEpicLogin}>Login</button>
        </div>
      )}

      <h3>GOG.com</h3>
      {gogStatus && gogStatus.logged_in ? (
        <div>
          <p>Logged in to GOG</p>
          <button onClick={handleGogLogout}>Logout</button>
        </div>
      ) : (
        <div>
          <p>Not logged in</p>
          <button onClick={handleGogLogin}>Login</button>
        </div>
      )}
    </div>
  );
}

export default Accounts;
