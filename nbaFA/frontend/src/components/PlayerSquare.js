import React from 'react';
import './PlayerSquare.css';

const PlayerSquare = ({ player, index, onClick, onRemove }) => {
  return (
    <div className="player-square" onClick={onClick}>
      {player ? (
        <div className="player-content">
          <div className="player-image-container">
            <img 
              src={player.imageUrl} 
              alt={player.name}
              className="player-image"
              onError={(e) => {
                e.target.src = 'https://via.placeholder.com/150x150/1a1a1a/ffffff?text=NBA';
              }}
            />
          </div>
          <div className="player-info">
            <h3 className="player-name">{player.name}</h3>
            <p className="player-position">{player.position}</p>
            <p className="player-team">{player.team}</p>
          </div>
          <button className="remove-player" onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}>
            ×
          </button>
        </div>
      ) : (
        <div className="empty-square">
          <div className="plus-icon">+</div>
          <p>Click to add player</p>
        </div>
      )}
    </div>
  );
};

export default PlayerSquare;
