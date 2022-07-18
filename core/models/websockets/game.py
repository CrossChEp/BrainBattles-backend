from typing import List, Dict

from starlette.websockets import WebSocket


class GameConnectionManager:
    def __init__(self):
        self.active_connections: Dict = {'token': [1]}

    async def connect(self, websocket: WebSocket, key_fraze: str):
        await websocket.accept()
        if not self.active_connections[key_fraze]:
            self.active_connections[key_fraze] = [websocket]
            return
        self.active_connections[key_fraze].apend(websocket)

    def disconnect(self, websocket: WebSocket, key_fraze: str):
        self.active_connections[key_fraze].remove(websocket)


