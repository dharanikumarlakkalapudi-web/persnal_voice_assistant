import React, { useEffect, useState } from 'react';

const FeaturesPanel: React.FC = () => {
  const [config, setConfig] = useState<any>(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8001/api/config')
      .then(res => res.json())
      .then(data => setConfig(data))
      .catch(err => console.error("Failed to load config:", err));
  }, []);

  const toggleFeature = (featureId: string, currentValue: boolean) => {
    fetch('http://127.0.0.1:8001/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: `features.${featureId}`, value: !currentValue })
    }).then(() => {
      setConfig((prev: any) => ({
        ...prev,
        features: {
          ...prev.features,
          [featureId]: !currentValue
        }
      }));
    });
  };

  if (!config) return <div className="panel-content">Loading...</div>;

  const features = [
    { id: 'voice_input', name: 'Voice Input', desc: 'Allow JARVIS to listen to microphone' },
    { id: 'vision', name: 'Computer Vision', desc: 'Allow JARVIS to see the screen' },
    { id: 'os_control', name: 'OS Control', desc: 'Allow JARVIS to run shell commands' },
    { id: 'web_search', name: 'Web Search', desc: 'Allow JARVIS to browse the internet' }
  ];

  return (
    <>
      <div className="panel-header">FEATURE MANAGER</div>
      <div className="panel-content">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {features.map(f => (
            <div key={f.id} style={featureCardStyle}>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 'bold', color: 'white' }}>{f.name}</div>
                <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{f.desc}</div>
              </div>
              <button 
                onClick={() => toggleFeature(f.id, config.features?.[f.id] ?? false)}
                style={{
                  ...toggleButtonStyle,
                  background: config.features?.[f.id] ? '#22c55e' : 'rgba(255,255,255,0.1)'
                }}
              >
                {config.features?.[f.id] ? 'ON' : 'OFF'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

const featureCardStyle = {
  display: 'flex',
  alignItems: 'center',
  background: 'rgba(0,0,0,0.2)',
  padding: '16px',
  borderRadius: '8px',
  border: '1px solid rgba(255,255,255,0.05)'
};

const toggleButtonStyle = {
  border: 'none',
  padding: '8px 16px',
  borderRadius: '20px',
  color: 'white',
  fontWeight: 'bold',
  cursor: 'pointer',
  transition: 'background 0.2s'
};

export default FeaturesPanel;
