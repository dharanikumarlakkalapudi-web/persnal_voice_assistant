import React from 'react';
import { useJarvisSocket } from '../hooks/useJarvisSocket';

const JarvisCore: React.FC = () => {
  const { voiceState } = useJarvisSocket();
  
  // Create some visual tick marks for the outer ring using an SVG
  const renderTicks = () => {
    const ticks = [];
    for (let i = 0; i < 72; i++) {
      const angle = i * 5;
      ticks.push(
        <line 
          key={i}
          x1="210" y1="20" x2="210" y2={i % 6 === 0 ? "0" : "10"} 
          stroke={i > 50 && i < 60 ? 'var(--accent-red)' : 'var(--text-accent)'} 
          strokeWidth="2"
          transform={`rotate(${angle} 210 210)`}
          opacity={i % 2 === 0 ? "0.8" : "0.3"}
        />
      );
    }
    return (
      <svg className="ring-tick" viewBox="0 0 420 420">
        {ticks}
      </svg>
    );
  };
  
  const generateSoundBars = () => {
    // Fake sound bars
    const bars = [];
    for (let i = 0; i < 40; i++) {
      const height = voiceState === 'SPEAKING' ? Math.random() * 20 + 5 : 4;
      bars.push(
        <div 
          key={i} 
          className="sound-bar" 
          style={{ height: `${height}px`, transition: 'height 0.1s ease' }} 
        />
      );
    }
    return <div className="sound-bars">{bars}</div>;
  };

  return (
    <div className="jarvis-orb-container">
      <div className="core-glow"></div>
      <div className="ring ring-1"></div>
      <div className="ring ring-2"></div>
      <div className="ring ring-3"></div>
      <div className="ring ring-4"></div>
      {renderTicks()}
      {generateSoundBars()}
    </div>
  );
};

export default JarvisCore;
