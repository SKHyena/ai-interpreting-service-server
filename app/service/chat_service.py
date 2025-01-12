from typing import Dict, List

from fastapi import WebSocket


class ChatManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, pairing_code: str, websocket: WebSocket):
        await websocket.accept()
        if pairing_code not in self.active_connections:
            self.active_connections[pairing_code] = []
        self.active_connections[pairing_code].append(websocket)

    def disconnect(self, pairing_code: str, websocket: WebSocket):
        if pairing_code in self.active_connections:
            self.active_connections[pairing_code].remove(websocket)

            if not self.active_connections[pairing_code]:
                self.active_connections.pop(pairing_code)

    async def broadcast_message(self, pairing_code: str, message: str):
        if pairing_code in self.active_connections:
            for connection in self.active_connections[pairing_code]:
                await connection.send_text(message)
