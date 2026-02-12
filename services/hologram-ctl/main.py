from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [HOLO-CTL] %(message)s')
logger = logging.getLogger("HologramController")

app = FastAPI(title="GABIZAP Holographic Stream")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("New AR Headset Connected.")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/stream/hologram")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # 1. 3D Global Threat Map Data
            threat_node = {
                "type": "THREAT_NODE",
                "coordinates": {
                    "lat": random.uniform(-90, 90),
                    "lon": random.uniform(-180, 180),
                    "alt": random.randint(0, 500) # km above earth
                },
                "severity": random.choice(["LOW", "MEDIUM", "CRITICAL"]),
                "vector": [random.random() for _ in range(3)] # 3D Vector
            }
            
            # 2. Volumetric Biometric Data (Simulated Point Cloud frame)
            # Sends a small burst of vertices for a "ghostly" effect
            point_cloud = {
                "type": "BIOMETRIC_CLOUD",
                "vertices": [
                    {"x": random.gauss(0, 1), "y": random.gauss(0, 1), "z": random.gauss(0, 1)}
                    for _ in range(50)
                ],
                "scan_id": f"SCAN-{random.randint(1000,9999)}"
            }
            
            await manager.broadcast(threat_node)
            await manager.broadcast(point_cloud)
            
            await asyncio.sleep(0.5) # 2fps update for demo
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("AR Headset Disconnected.")
