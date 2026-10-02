import React, { useState, useEffect, useRef } from 'react';
import { useJarvisSocket } from '../hooks/useJarvisSocket';

const HomePanel: React.FC = () => {
  const { transcript, aiResponse } = useJarvisSocket();
  const [messages, setMessages] = useState<{role: 'user' | 'jarvis', text: string}[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (transcript && transcript.text.trim() !== '') {
      setMessages(prev => [...prev, { role: 'user', text: transcript.text }]);
    }
  }, [transcript]);

  useEffect(() => {
    if (aiResponse && aiResponse.text.trim() !== '') {
      setMessages(prev => [...prev, { role: 'jarvis', text: aiResponse.text }]);
    }
  }, [aiResponse]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <>
      <div className="panel-header">• TRANSCRIPT</div>
      <div className="panel-content">
        {messages.map((msg, idx) => (
          <div key={idx} className={`transcript-line ${msg.role}`}>
            <span className="speaker">{msg.role === 'user' ? 'USR' : 'DEX'}</span>
            <span>{msg.text}</span>
          </div>
        ))}
        {transcript && (
          <div className="transcript-line user" style={{ opacity: 0.5 }}>
             <span className="speaker">USR</span>
             <span>{transcript.text}...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
    </>
  );
};

export default HomePanel;
