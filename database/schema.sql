-- JARVIS V2 Platform Schema

-- Table for storing system configuration metadata (e.g., schema version)
CREATE TABLE IF NOT EXISTS schema_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Table for storing agent identities
CREATE TABLE IF NOT EXISTS agents (
    agent_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    permissions_profile TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT 1,
    system_instructions TEXT
);

-- Table for storing application registry
CREATE TABLE IF NOT EXISTS applications (
    app_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    app_type TEXT NOT NULL,
    launch_method TEXT NOT NULL,
    executable_path TEXT,
    arguments TEXT,
    working_directory TEXT,
    enabled BOOLEAN NOT NULL DEFAULT 1
);

-- Table for feature toggles
CREATE TABLE IF NOT EXISTS features (
    feature_id TEXT PRIMARY KEY,
    enabled BOOLEAN NOT NULL DEFAULT 1,
    dependencies TEXT -- JSON list of required feature_ids
);

-- Table for hotkey bindings
CREATE TABLE IF NOT EXISTS hotkeys (
    action_id TEXT PRIMARY KEY,
    key_combination TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT 1
);

-- Table for security profiles
CREATE TABLE IF NOT EXISTS profiles (
    profile_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    description TEXT
);

-- Table for long-term memories
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT,
    importance INTEGER DEFAULT 1
);

-- Table for activity logs
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_id TEXT,
    tool_id TEXT,
    action TEXT,
    risk_level INTEGER,
    permission_decision TEXT,
    result TEXT
);

-- Insert initial schema version
INSERT OR IGNORE INTO schema_metadata (key, value) VALUES ('schema_version', '1');
