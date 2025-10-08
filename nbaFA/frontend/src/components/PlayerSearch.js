import React, { useState, useEffect } from 'react';
import './PlayerSearch.css';

// Mock NBA player data - in a real app, this would come from an API
const mockPlayers = [
  { id: 1, name: 'LeBron James', position: 'SF', team: 'Lakers', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png' },
  { id: 2, name: 'Stephen Curry', position: 'PG', team: 'Warriors', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/201939.png' },
  { id: 3, name: 'Kevin Durant', position: 'SF', team: 'Suns', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/201142.png' },
  { id: 4, name: 'Giannis Antetokounmpo', position: 'PF', team: 'Bucks', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203507.png' },
  { id: 5, name: 'Luka Doncic', position: 'PG', team: 'Mavericks', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png' },
  { id: 6, name: 'Jayson Tatum', position: 'SF', team: 'Celtics', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1628369.png' },
  { id: 7, name: 'Joel Embiid', position: 'C', team: '76ers', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203954.png' },
  { id: 8, name: 'Nikola Jokic', position: 'C', team: 'Nuggets', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203999.png' },
  { id: 9, name: 'Jimmy Butler', position: 'SF', team: 'Heat', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/202710.png' },
  { id: 10, name: 'Anthony Davis', position: 'PF', team: 'Lakers', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203076.png' },
  { id: 11, name: 'Kawhi Leonard', position: 'SF', team: 'Clippers', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/202695.png' },
  { id: 12, name: 'Damian Lillard', position: 'PG', team: 'Bucks', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203081.png' },
  { id: 13, name: 'Paul George', position: 'SF', team: 'Clippers', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/202331.png' },
  { id: 14, name: 'Russell Westbrook', position: 'PG', team: 'Clippers', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/201566.png' },
  { id: 15, name: 'Kyrie Irving', position: 'PG', team: 'Mavericks', imageUrl: 'https://cdn.nba.com/headshots/nba/latest/1040x760/202681.png' }
];

const PlayerSearch = ({ onPlayerSelect, onClose }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredPlayers, setFilteredPlayers] = useState(mockPlayers);

  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredPlayers(mockPlayers);
    } else {
      const filtered = mockPlayers.filter(player =>
        player.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        player.team.toLowerCase().includes(searchTerm.toLowerCase()) ||
        player.position.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredPlayers(filtered);
    }
  }, [searchTerm]);

  const handlePlayerClick = (player) => {
    onPlayerSelect(player);
  };

  return (
    <div className="search-overlay">
      <div className="search-modal">
        <div className="search-header">
          <h2>Search NBA Players</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        
        <div className="search-input-container">
          <input
            type="text"
            placeholder="Search by name, team, or position..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
            autoFocus
          />
        </div>
        
        <div className="search-results">
          {filteredPlayers.length > 0 ? (
            filteredPlayers.map(player => (
              <div
                key={player.id}
                className="search-result-item"
                onClick={() => handlePlayerClick(player)}
              >
                <img
                  src={player.imageUrl}
                  alt={player.name}
                  className="result-player-image"
                  onError={(e) => {
                    e.target.src = 'https://via.placeholder.com/50x50/1a1a1a/ffffff?text=NBA';
                  }}
                />
                <div className="result-player-info">
                  <h4>{player.name}</h4>
                  <p>{player.position} • {player.team}</p>
                </div>
              </div>
            ))
          ) : (
            <div className="no-results">
              <p>No players found matching "{searchTerm}"</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PlayerSearch;
