import { useEffect, useState } from 'react';

export interface JarvisState {
  isConnected: boolean;
  voiceState: 'IDLE' | 'LISTENING' | 'PROCESSING' | 'SPEAKING' | 'OFFLINE';
  transcript: { text: string; ts: number } | null;
  aiResponse: { text: string; ts: number } | null;
  currentAgent: string;
  systemMetrics: {
    cpu: number;
    ram: number;
    mic: boolean;
    camera: boolean;
    security: boolean;
  };
}

export function useJarvisSocket() {
  const [state, setState] = useState<JarvisState>({
    isConnected: false,
    voiceState: 'OFFLINE',
    transcript: null,
    aiResponse: null,
    currentAgent: 'PERSONAL',
    systemMetrics: {
      cpu: 0,
      ram: 0,
      mic: false,
      camera: false,
      security: true
    }
  });

  useEffect(() => {
    let socket: WebSocket;
    let reconnectTimer: number;

    const connect = () => {
      socket = new WebSocket('ws://127.0.0.1:8001/ws');

      socket.onopen = () => {
        setState(prev => ({ ...prev, isConnected: true, voiceState: 'IDLE' }));
      };

      socket.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          
          if (payload.type === 'voice.state') {
            setState(prev => ({ ...prev, voiceState: payload.data.state }));
          } else if (payload.type === 'voice.transcript') {
            setState(prev => ({ ...prev, transcript: { text: payload.data.text, ts: Date.now() } }));
          } else if (payload.type === 'voice.response') {
            setState(prev => ({ ...prev, aiResponse: { text: payload.data.text, ts: Date.now() } }));
          } else if (payload.type === 'agent.changed') {
            setState(prev => ({ ...prev, currentAgent: payload.data.agent_id.toUpperCase() }));
          } else if (payload.type === 'system.metrics') {
            setState(prev => ({ ...prev, systemMetrics: payload.data }));
          }
        } catch (e) {
          console.error("Failed to parse socket message", e);
        }
      };

      socket.onclose = () => {
        setState(prev => ({ ...prev, isConnected: false, voiceState: 'OFFLINE' }));
        reconnectTimer = window.setTimeout(connect, 3000);
      };
      
      socket.onerror = () => {
        socket.close();
      };
    };

    connect();

    return () => {
      clearTimeout(reconnectTimer);
      if (socket) socket.close();
    };
  }, []);

  return state;
}
