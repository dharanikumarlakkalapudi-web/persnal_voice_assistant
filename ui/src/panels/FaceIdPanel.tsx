import React, { useEffect, useState } from 'react';

const FaceIdPanel: React.FC = () => {
  const [config, setConfig] = useState<any>(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8001/api/config')
      .then(res => res.json())
      .then(data => setConfig(data))
      .catch(err => console.error("Failed to load config:", err));
  }, []);

  const updateSecurityLevel = (level: string) => {
    fetch('http://127.0.0.1:8001/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: 'security.level', value: level })
    }).then(() => {
      setConfig((prev: any) => ({
        ...prev,
        security: { ...prev.security, level }
      }));
    });
  };

  if (!config) return <div className="panel-content">Loading...</div>;

  const currentLevel = config.security?.level || 'balanced';

  return (
    <>
      <div className="panel-header">FACE ID SECURITY</div>
      <div className="panel-content">
        
        <div style={{ background: 'rgba(0,0,0,0.2)', padding: '20px', borderRadius: '8px', textAlign: 'center', marginBottom: '24px' }}>
          <div style={{ color: '#22c55e', fontWeight: 'bold', marginBottom: '8px' }}>● CONFIGURED</div>
          <div style={{ color: 'var(--text-muted)', fontSize: '14px', marginBottom: '16px' }}>Active User: {config.identity?.user_name || 'User'}</div>
          <button style={{ 
            background: 'transparent', 
            color: 'white', 
            border: '1px solid rgba(255,255,255,0.2)', 
            padding: '8px 20px', 
            borderRadius: '6px',
            cursor: 'pointer'
          }}>TEST FACE ID</button>
        </div>

        <h3 style={{ marginBottom: '16px', color: 'var(--text-accent)' }}>SECURITY LEVEL</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '32px' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <input type="radio" name="level" checked={currentLevel === 'relaxed'} onChange={() => updateSecurityLevel('relaxed')} /> Relaxed
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <input type="radio" name="level" checked={currentLevel === 'balanced'} onChange={() => updateSecurityLevel('balanced')} /> Balanced
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <input type="radio" name="level" checked={currentLevel === 'strict'} onChange={() => updateSecurityLevel('strict')} /> Strict
          </label>
        </div>

        <h3 style={{ marginBottom: '16px', color: 'var(--text-accent)' }}>PROTECTED ACTIONS</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={protectedActionStyle}><span>Shutdown</span> <span>🔒</span></div>
          <div style={protectedActionStyle}><span>PowerShell</span> <span>🔒</span></div>
          <div style={protectedActionStyle}><span>System changes</span> <span>🔒</span></div>
          <div style={protectedActionStyle}><span>Credential changes</span> <span>🔒</span></div>
        </div>

      </div>
    </>
  );
};

const protectedActionStyle = {
  display: 'flex', 
  justifyContent: 'space-between', 
  padding: '12px', 
  background: 'rgba(0,0,0,0.1)', 
  borderRadius: '6px',
  border: '1px solid rgba(255,255,255,0.05)'
};

export default FaceIdPanel;
