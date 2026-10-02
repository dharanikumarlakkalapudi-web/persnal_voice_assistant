import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Sliders, ScanFace, Cpu, LayoutGrid, BookOpen } from 'lucide-react';

const Sidebar: React.FC = () => {
  return (
    <aside className="sidebar glass-panel">
      <h1>JARVIS <span>V2</span></h1>
      
      <nav className="nav-menu">
        <NavLink to="/home" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Home size={18} />
          HOME
        </NavLink>
        <NavLink to="/controls" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Sliders size={18} />
          CONTROLS
        </NavLink>
        <NavLink to="/face-id" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <ScanFace size={18} />
          FACE ID
        </NavLink>
        <NavLink to="/ai-models" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Cpu size={18} />
          AI MODELS
        </NavLink>
        <NavLink to="/features" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <LayoutGrid size={18} />
          FEATURES
        </NavLink>
        <NavLink to="/manual" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <BookOpen size={18} />
          USER MANUAL
        </NavLink>
      </nav>
    </aside>
  );
};

export default Sidebar;
