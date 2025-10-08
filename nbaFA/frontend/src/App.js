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
          <button className="calculate-button" onClick={() => console.log('Calculate clicked!', players.filter(p => p !== null))}>
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
