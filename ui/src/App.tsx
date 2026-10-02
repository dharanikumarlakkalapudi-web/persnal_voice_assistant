import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import HomePanel from './panels/HomePanel';
import JarvisCore from './components/JarvisCore';
import { useJarvisSocket } from './hooks/useJarvisSocket';
import './theme.css';

function App() {
  const { voiceState } = useJarvisSocket();
  return (
    <BrowserRouter>
      <div className="app-shell">
        <header className="top-header">
          <h1>JARVIS</h1>
          <div className="subtitle">VOICE INTERFACE</div>
        </header>

        <main className="main-area">
          <div className="gauges-container">
            <div className="gauge">CPU</div>
            <div className="gauge">MEM</div>
          </div>
          <JarvisCore />
        </main>
        
        <aside className="right-panel">
          <Routes>
            <Route path="/" element={<Navigate to="/home" replace />} />
            <Route path="/home" element={<HomePanel />} />
            {/* Fallback for empty routes */}
            <Route path="*" element={<div className="panel-content">Under Construction</div>} />
          </Routes>
        </aside>

        <div className="bottom-left-status">
          <div className="status-dot"></div>
          {voiceState === 'LISTENING' ? 'LISTENING_' : voiceState === 'SPEAKING' ? 'SPEAKING_' : voiceState === 'PROCESSING' ? 'PROCESSING_' : 'IDLE_'}
        </div>

        <div className="bottom-right-controls">
          <button className="cyber-btn">MUTE</button>
          <button className="cyber-btn">INTERRUPT OFF</button>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
