import React, { useEffect, useState } from 'react';

const AiModelsPanel: React.FC = () => {
  const [config, setConfig] = useState<any>(null);
  const [groqKey, setGroqKey] = useState('');
  const [openAiKey, setOpenAiKey] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8001/api/config')
      .then(res => res.json())
      .then(data => setConfig(data))
      .catch(err => console.error("Failed to load config:", err));
  }, []);

  const updateProvider = (provider: string) => {
    fetch('http://127.0.0.1:8001/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: 'ai.default_provider', value: provider })
    }).then(() => {
      setConfig((prev: any) => ({
        ...prev,
        ai: { ...prev.ai, default_provider: provider }
      }));
    });
  };

  const saveSecret = (service: string, key: string) => {
    fetch('http://127.0.0.1:8001/api/secrets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ service: service, username: 'api_key', password: key })
    }).then(() => {
      alert(`${service} Key Saved Securely to Windows DPAPI Vault!`);
      if (service === 'groq') setGroqKey('');
      if (service === 'openai') setOpenAiKey('');
    });
  };

  if (!config) return <div className="panel-content">Loading...</div>;

  return (
    <>
      <div className="panel-header">AI PROVIDERS</div>
      <div className="panel-content">
        
        <h3 style={{ marginBottom: '16px', color: 'var(--text-accent)' }}>DEFAULT ENGINE</h3>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '32px' }}>
          <button 
            onClick={() => updateProvider('groq')}
            style={{
              ...providerBtnStyle,
              borderColor: config.ai?.default_provider === 'groq' ? '#0ea5e9' : 'rgba(255,255,255,0.1)',
              background: config.ai?.default_provider === 'groq' ? 'rgba(14,165,233,0.1)' : 'rgba(0,0,0,0.2)'
            }}
          >
            GROQ (Llama 3)
          </button>
          <button 
            onClick={() => updateProvider('openai')}
            style={{
              ...providerBtnStyle,
              borderColor: config.ai?.default_provider === 'openai' ? '#0ea5e9' : 'rgba(255,255,255,0.1)',
              background: config.ai?.default_provider === 'openai' ? 'rgba(14,165,233,0.1)' : 'rgba(0,0,0,0.2)'
            }}
          >
            OpenAI (GPT-4)
          </button>
        </div>

        <h3 style={{ marginBottom: '16px', color: 'var(--text-accent)' }}>API KEYS (SECURE VAULT)</h3>
        
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-muted)', marginBottom: '4px' }}>Groq API Key</label>
          <div style={{ display: 'flex', gap: '10px' }}>
            <input 
              type="password" 
              placeholder="gsk_..." 
              value={groqKey}
              onChange={(e) => setGroqKey(e.target.value)}
              style={inputStyle} 
            />
            <button onClick={() => saveSecret('groq', groqKey)} style={saveBtnStyle}>SAVE</button>
          </div>
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-muted)', marginBottom: '4px' }}>OpenAI API Key</label>
          <div style={{ display: 'flex', gap: '10px' }}>
            <input 
              type="password" 
              placeholder="sk-..." 
              value={openAiKey}
              onChange={(e) => setOpenAiKey(e.target.value)}
              style={inputStyle} 
            />
            <button onClick={() => saveSecret('openai', openAiKey)} style={saveBtnStyle}>SAVE</button>
          </div>
        </div>

      </div>
    </>
  );
};

const providerBtnStyle = {
  flex: 1,
  padding: '16px',
  borderRadius: '8px',
  border: '2px solid',
  color: 'white',
  fontWeight: 'bold',
  cursor: 'pointer',
  transition: 'all 0.2s'
};

const inputStyle = {
  flex: 1,
  background: 'rgba(0,0,0,0.2)',
  border: '1px solid rgba(255,255,255,0.1)',
  padding: '10px',
  borderRadius: '6px',
  color: 'white',
  outline: 'none'
};

const saveBtnStyle = {
  background: '#22c55e',
  color: 'white',
  border: 'none',
  padding: '0 16px',
  borderRadius: '6px',
  fontWeight: 'bold',
  cursor: 'pointer'
};

export default AiModelsPanel;
