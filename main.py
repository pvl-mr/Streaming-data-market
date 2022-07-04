import asyncio
from fastapi import FastAPI, WebSocket
from random import random

app = FastAPI()

tickers = [f't{i}' for i in range(20)]


@app.get('/stocks')
def stocks():
    return {'tickers': tickers}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data not in tickers:
                resp = {'details': 'no data'}
                await websocket.send_json(resp)
                break
            await asyncio.sleep(1)
            current_price = 0
            payload = current_price + generate_movement()
            await websocket.send_json({"ticker": data, "price": payload})
    except Exception as e:
        print('error:', e)


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement
