import React, { useState, useEffect } from 'react';
import api from '../api';

function Accounts({ token }) {
  const [amazonStatus, setAmazonStatus] = useState(null);

  useEffect(() => {
    const fetchAmazonStatus = async () => {
      try {
        const { data } = await api.get('/accounts/amazon/status');
        setAmazonStatus(data);
      } catch (err) {
        console.error("Failed to fetch Amazon status", err);
      }
    };
    fetchAmazonStatus();
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
    </div>
  );
}

export default Accounts;
