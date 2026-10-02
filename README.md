# Jarvis: Personal Voice Assistant

Jarvis is a highly capable personal voice assistant built with a Python backend and a React/TypeScript frontend. It integrates various AI models, computer vision for Face ID authentication, voice recognition, and proactive agentic capabilities.

## 🚀 Features

- **Face ID & Voice Authentication**: Secure, seamless access using advanced face detection (Yunet) and recognition (SFace).
- **Proactive Agents**: Runs background workers that anticipate your needs and provide context-aware suggestions.
- **Multi-Modal AI**: Specialized agents for vision, coding, general tasks, and integrations.
- **Modern Web UI**: A sleek, Vite+React-based web interface for monitoring and interacting with the system.
- **Modular Architecture**: Built with highly decoupled components (Agents, Core, Configuration, Integrations, Security, Tools, and Vision).
- **Rich Integrations**: Natively supports Gmail, Google Calendar, and more.

## 📂 Architecture

For a deep dive into how Jarvis works, check out the [ARCHITECTURE.md](ARCHITECTURE.md) and [JARVIS_CAPABILITIES.md](JARVIS_CAPABILITIES.md) files.

- `agents/`: Contains specialized AI agents.
- `core/`: The central orchestrator, event bus, and application lifecycle management.
- `security/`: Handles credential vaulting, Face ID, and overall security management.
- `ui/`: The Vite + React + TS frontend for the assistant.
- `integrations/`: Third-party service connections (Google APIs, etc.).

## 🛠️ Prerequisites

- **Python 3.9+**
- **Node.js 18+** (for the UI)
- The necessary `.onnx` and `.pt` machine learning models (these are ignored by git due to size and must be placed in the project root/appropriate folders).

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dharanikumarlakkalapudi-web/persnal_voice_assistant.git
   cd persnal_voice_assistant
   ```

2. **Backend Setup:**
   ```bash
   # Create and activate a virtual environment
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On Mac/Linux: source venv/bin/activate
   
   # Install dependencies (assuming you have a requirements.txt or pipfile)
   pip install -r requirements.txt
   ```

3. **Frontend Setup:**
   ```bash
   cd ui
   npm install
   npm run dev
   ```

4. **Environment Variables:**
   Copy `.env.example` to `.env` and fill in your API keys and configuration parameters.

## 🚀 Usage

Start the main application backend:
```bash
python main.py
```
This command initializes the event bus, spins up the AI orchestrator, and starts the server for the UI to connect via websockets.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
