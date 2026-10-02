import React from 'react';
import { useJarvisSocket } from '../hooks/useJarvisSocket';

const StatusBar: React.FC = () => {
  const { isConnected, systemMetrics } = useJarvisSocket();

  return (
    <div className="status-bar glass-panel">
      <div className="status-metric">
        <div className={`indicator ${isConnected ? 'online' : 'offline'}`}></div>
        {isConnected ? 'ONLINE' : 'OFFLINE'}
      </div>
      <div className="status-metric">CPU {systemMetrics.cpu}%</div>
      <div className="status-metric">RAM {systemMetrics.ram} GB</div>
      <div className="status-metric">
        MIC <div className={`indicator ${systemMetrics.mic ? 'online' : 'offline'}`}></div>
      </div>
      <div className="status-metric">
        CAMERA <div className={`indicator ${systemMetrics.camera ? 'online' : 'offline'}`}></div>
      </div>
      <div className="status-metric">
        SECURITY <div className={`indicator ${systemMetrics.security ? 'online' : 'offline'}`}></div>
      </div>
    </div>
  );
};

export default StatusBar;
