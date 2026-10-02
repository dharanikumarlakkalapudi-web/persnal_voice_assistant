import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

const ManualPanel: React.FC = () => {
  const [content, setContent] = useState<string>('Loading manual...');

  useEffect(() => {
    fetch('http://127.0.0.1:8001/api/manual')
      .then(res => res.json())
      .then(data => setContent(data.content))
      .catch(err => setContent(`# Error loading manual\n${err}`));
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="panel-header">JARVIS USER MANUAL</div>
      <div className="panel-content" style={{ overflowY: 'auto', paddingRight: '10px' }}>
        <div className="markdown-body">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

// Global CSS overrides for Markdown elements can be placed in theme.css
export default ManualPanel;
