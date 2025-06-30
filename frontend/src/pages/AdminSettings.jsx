import React, { useState, useEffect } from 'react';
import api from '../api';

function AdminSettings() {
  const [settings, setSettings] = useState({});
  const [autoClaim, setAutoClaim] = useState(3600);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const { data } = await api.get('/admin/settings');
        setSettings(data);
        setAutoClaim(data.auto_claim_interval || 3600);
      } catch (err) {
        console.error("Failed to fetch settings", err);
      }
    };
    fetchSettings();
  }, []);

  const handleSave = async () => {
    try {
      await api.post('/admin/settings', { auto_claim_interval: autoClaim });
      alert('Settings updated');
    } catch (err) {
      alert('Failed to update settings');
    }
  };

  return (
    <div>
      <h3>Admin Settings</h3>
      <div>
        <label>Auto Claim Interval (seconds)</label>
        <input
          type="number"
          value={autoClaim}
          onChange={(e) => setAutoClaim(e.target.value)}
        />
        <button onClick={handleSave}>Save</button>
      </div>
    </div>
  );
}

export default AdminSettings;
