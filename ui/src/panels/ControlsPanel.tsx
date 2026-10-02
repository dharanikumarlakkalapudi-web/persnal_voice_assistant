import React, { useEffect, useState } from 'react';

const ControlsPanel: React.FC = () => {
  const [config, setConfig] = useState<any>(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8001/api/config')
      .then(res => res.json())
      .then(data => setConfig(data))
      .catch(err => console.error("Failed to load config:", err));
  }, []);

  const updateConfig = (path: string, value: any) => {
    fetch('http://127.0.0.1:8001/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path, value })
    }).then(() => {
      setConfig((prev: any) => {
        const newConfig = { ...prev };
        const parts = path.split('.');
        let current = newConfig;
        for (let i = 0; i < parts.length - 1; i++) {
          if (!current[parts[i]]) current[parts[i]] = {};
          current = current[parts[i]];
        }
        current[parts[parts.length - 1]] = value;
        return newConfig;
      });
    });
  };

  if (!config) return <div className="panel-content">Loading...</div>;

  return (
    <>
      <div className="panel-header">CONTROLS & SETTINGS</div>
      <div className="panel-content">
        <h3 style={{ marginBottom: '16px', color: 'var(--text-accent)' }}>IDENTITY</h3>
        <div style={{ display: 'grid', gap: '12px', marginBottom: '32px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-muted)', marginBottom: '4px' }}>JARVIS Display Name</label>
            <input 
              type="text" 
              value={config.identity?.assistant_name || ''} 
              onChange={(e) => updateConfig('identity.assistant_name', e.target.value)}
              style={inputStyle} 
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-muted)', marginBottom: '4px' }}>User Name</label>
            <input 
              type="text" 
              value={config.identity?.user_name || ''} 
              onChange={(e) => updateConfig('identity.user_name', e.target.value)}
              style={inputStyle} 
            />
          </div>
        </div>
        
        <h3 style={{ marginBottom: '16px', color: 'var(--text-accent)' }}>ACTIVATION</h3>
        <div style={{ display: 'grid', gap: '12px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-muted)', marginBottom: '4px' }}>Wake Words (comma separated)</label>
            <input 
              type="text" 
              value={(config.activation?.wake_words || []).join(', ')} 
              onChange={(e) => {
                const val = e.target.value;
                // Update local state for smooth typing, save array to backend
                const arr = val.split(',').map(s => s.trim()).filter(s => s.length > 0);
                updateConfig('activation.wake_words', arr);
                
                // Keep local state sync so commas aren't deleted while typing
                setConfig((prev: any) => ({
                    ...prev,
                    activation: {
                        ...prev.activation,
                        wake_words: val.split(',')
                    }
                }));
              }}
              style={inputStyle} 
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-muted)', marginBottom: '4px' }}>Global Hotkey</label>
            <input 
              type="text" 
              value={config.activation?.hotkey || ''} 
              onChange={(e) => updateConfig('activation.hotkey', e.target.value)}
              style={inputStyle} 
            />
          </div>
        </div>
      </div>
    </>
  );
};

const inputStyle = {
  width: '100%',
  background: 'rgba(0,0,0,0.2)',
  border: '1px solid rgba(255,255,255,0.1)',
  padding: '10px',
  borderRadius: '6px',
  color: 'white',
  outline: 'none'
};

export default ControlsPanel;
