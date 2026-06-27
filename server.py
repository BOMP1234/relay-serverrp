import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

clients = []

@app.websocket("/ws")
async def relay(websocket: WebSocket):
    await websocket.accept()

    clients.append(websocket)
    print("Client connected")

    try:
        while True:
            data = await websocket.receive_text()

            for client in clients:
                if client != websocket:
                    await client.send_text(data)

    except WebSocketDisconnect:
        print("Client disconnected")
        clients.remove(websocket)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
