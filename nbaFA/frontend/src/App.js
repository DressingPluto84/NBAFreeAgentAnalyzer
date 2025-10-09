import React, { useState } from 'react';
import './App.css';
import PlayerSquare from './components/PlayerSquare';
import PlayerSearch from './components/PlayerSearch';

function App() {
  const [players, setPlayers] = useState(Array(5).fill(null));
  const [showSearch, setShowSearch] = useState(false);
  const [selectedSquare, setSelectedSquare] = useState(null);

  const handleSquareClick = (index) => {
    setSelectedSquare(index);
    setShowSearch(true);
  };

  const handlePlayerSelect = (player) => {
    const newPlayers = [...players];
    newPlayers[selectedSquare] = player;
    setPlayers(newPlayers);
    setShowSearch(false);
    setSelectedSquare(null);
  };

  const handleCloseSearch = () => {
    setShowSearch(false);
    setSelectedSquare(null);
  };

  const handleRemovePlayer = (index) => {
    const newPlayers = [...players];
    newPlayers[index] = null;
    setPlayers(newPlayers);
  };

  const handleCalculate = async () => {
    const selectedPlayers = players.filter(player => player !== null);
    
    if (selectedPlayers.length === 0) {
      alert('Please select at least one player before calculating.');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/players', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          players: selectedPlayers.map(player => player.name)
        })
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Calculation result:', result);
        // You can add more UI feedback here
      } else {
        console.error('Error:', response.statusText);
        alert('Error calculating player analysis. Please try again.');
      }
    } catch (error) {
      console.error('Network error:', error);
      alert('Unable to connect to the backend server. Please make sure it is running.');
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>NBA Free Agent Analyzer</h1>
        <p>Select up to 5 NBA players to analyze</p>
      </header>
      
      <main className="player-selection">
        <div className="player-grid">
          {players.map((player, index) => (
            <PlayerSquare
              key={index}
              player={player}
              index={index}
              onClick={() => handleSquareClick(index)}
              onRemove={() => handleRemovePlayer(index)}
            />
          ))}
        </div>
        
        <div className="calculate-section">
          <button className="calculate-button" onClick={handleCalculate}>
            Calculate
          </button>
        </div>
      </main>

      {showSearch && (
        <PlayerSearch
          onPlayerSelect={handlePlayerSelect}
          onClose={handleCloseSearch}
        />
      )}
    </div>
  );
}

export default App;
