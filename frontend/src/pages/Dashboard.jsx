import React, { useState, useEffect } from 'react';
import api from '../api';

function Dashboard({ user }) {
  const [games, setGames] = useState([]);

  useEffect(() => {
    const fetchGames = async () => {
      try {
        const { data } = await api.get('/games');
        setGames(data);
      } catch (err) {
        console.error("Failed to fetch games", err);
      }
    };
    fetchGames();
  }, []);

  return (
    <div>
      <h2>Welcome {user.username}</h2>
      <h3>Your Games:</h3>
      <ul>
        {games.map(game => (
          <li key={game.id}>{game.title} - {game.claimed ? 'Claimed' : 'Not Claimed'}</li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
