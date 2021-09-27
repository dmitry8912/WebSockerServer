import os
import json
import asyncio
import websockets
from websockets import exceptions
from jsonrpc import JSONRPCResponseManager, dispatcher

# Set of connected clients
clients = set()

# Global application configuration
app_conf = {}


def config():
    app_config = {
        "host": None,
        "port": 8765
    }
    if 'WSS_HOST' in os.environ:
        app_config["host"] = os.environ['WSS_HOST']
    if 'WSS_PORT' in os.environ:
        app_config["port"] = os.environ['WSS_PORT']
    return app_config


# Message broadcasting, sends a message to all connected clients
async def broadcast(message, **kwargs):
    clients_copy = clients.copy()
    for websocket in clients_copy:
        try:
            await websocket.send(message)
        except websockets.ConnectionClosed:
            clients.remove(websocket)


@dispatcher.add_method
def send_echo(message):
    # Form a JSON to client, not plain text
    return {"message": message}


@dispatcher.add_method
def send_message(ids, message):
    asyncio.get_event_loop().create_task(
        broadcast(
            json.dumps({"message": message})
        )
    )
    return True


async def consume(message, request_websocket):
    await request_websocket.send(json.dumps(JSONRPCResponseManager.handle(message, dispatcher).data))


# Handler for websocket messages
async def handler(websocket, path):
    # Basically, add any client to set of clients
    clients.add(websocket)
    try:
        async for message in websocket:
            await consume(message, websocket)
    # If client disconnects - remove him from set of currently connected clients
    except websockets.exceptions.ConnectionClosedError:
        clients.remove(websocket)


async def main():
    async with websockets.serve(handler, app_conf["host"], app_conf["port"]):
        await asyncio.Future()


if __name__ == '__main__':
    app_conf = config()
    print(f"Running at {app_conf['host']} on {app_conf['port']}")
    asyncio.run(main())
