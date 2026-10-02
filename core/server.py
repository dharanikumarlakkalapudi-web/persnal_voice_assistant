from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from core.event_bus import event_bus
from configuration.manager import config_manager
from security.credential_vault import vault
from pydantic import BaseModel
from typing import Any, Dict
import asyncio
import json

app = FastAPI()

# Allow React app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"[WebSocket] Client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"[WebSocket] Client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, event_type: str, data: dict):
        if not self.active_connections:
            return
            
        message = json.dumps({"type": event_type, "data": data})
        
        # Create a list of tasks for sending messages
        tasks = []
        for connection in self.active_connections:
            tasks.append(connection.send_text(message))
            
        # Run them concurrently and handle potential disconnections
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.disconnect(self.active_connections[i])

manager = ConnectionManager()

# We need an async queue to bridge synchronous Python threads (EventBus) to AsyncIO WebSockets
event_queue = None
main_loop = None

def sync_event_handler(event_type: str, data: dict):
    """Called by EventBus synchronously in random threads. We push to asyncio queue."""
    if main_loop and main_loop.is_running() and event_queue:
        asyncio.run_coroutine_threadsafe(event_queue.put((event_type, data)), main_loop)

@app.on_event("startup")
async def startup_event():
    global main_loop, event_queue
    main_loop = asyncio.get_running_loop()
    event_queue = asyncio.Queue()
    
    # Subscribe the bridge to all events
    known_events = [
        "voice.state", "voice.transcript", "voice.response", "system.metrics", "agent.changed"
    ]
    for e in known_events:
        event_bus.subscribe(e, sync_event_handler)
    
    # Start the background broadcasting task
    asyncio.create_task(broadcast_loop())

async def broadcast_loop():
    """Continuously reads from the thread-safe queue and broadcasts via WebSockets."""
    while True:
        event_type, data = await event_queue.get()
        await manager.broadcast(event_type, data)

class ConfigPayload(BaseModel):
    path: str
    value: Any

class SecretPayload(BaseModel):
    service: str
    username: str
    password: str

@app.get("/api/config")
async def get_config():
    return config_manager.config

@app.post("/api/config")
async def update_config(payload: ConfigPayload):
    config_manager.set(payload.path, payload.value)
    # Broadcast config change event if needed
    if loop := asyncio.get_event_loop():
        if loop.is_running():
            loop.call_soon_threadsafe(event_queue.put_nowait, ("config.changed", {"path": payload.path}))
    return {"status": "success", "config": config_manager.config}

@app.post("/api/secrets")
async def save_secret(payload: SecretPayload):
    vault.set_credential(f"{payload.service}_api_key", payload.password)
    return {"status": "success"}

@app.get("/api/manual")
async def get_manual():
    import os
    try:
        with open(os.path.join(os.path.dirname(__file__), "..", "JARVIS_CAPABILITIES.md"), "r") as f:
            return {"content": f.read()}
    except Exception as e:
        return {"content": f"# Error loading manual\n{e}"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We don't really expect messages from the client yet, just heartbeat
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Mount React App static files
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

ui_dist_path = os.path.join(os.path.dirname(__file__), "..", "ui", "dist")

if os.path.exists(ui_dist_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(ui_dist_path, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # Serve index.html for unknown routes to support client-side routing
        potential_file = os.path.join(ui_dist_path, full_path)
        if os.path.isfile(potential_file):
            return FileResponse(potential_file, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
        return FileResponse(os.path.join(ui_dist_path, "index.html"), headers={"Cache-Control": "no-cache, no-store, must-revalidate"})

