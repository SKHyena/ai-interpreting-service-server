from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..service.chat_service import ChatManager

router = APIRouter()
manager = ChatManager()

@router.websocket("/{pairing_code}")
async def websocket_endpoint(websocket: WebSocket, pairing_code: str):
    await manager.connect(pairing_code, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast_message(pairing_code, data)

    except WebSocketDisconnect:
        manager.disconnect(pairing_code, websocket)
        await manager.send_message(pairing_code, "A user has disconnected.")
