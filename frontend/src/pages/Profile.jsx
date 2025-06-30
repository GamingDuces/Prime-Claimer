import React, { useState } from 'react';
import api from '../api';

function Profile({ user, token }) {
  const [discord, setDiscord] = useState(user.discord || '');
  const [email, setEmail] = useState(user.email || '');

  const handleSave = async () => {
    try {
      await api.put('/me', { discord, email });
      alert('Profile updated');
    } catch (err) {
      alert('Failed to update profile');
    }
  };

  return (
    <div>
      <h2>Your Profile</h2>
      <input
        type="text"
        placeholder="Discord"
        value={discord}
        onChange={(e) => setDiscord(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={handleSave}>Save</button>
    </div>
  );
}

export default Profile;
