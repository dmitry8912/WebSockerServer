import os
import asyncio
import websockets
from websockets import exceptions

# Set of connected clients
clients = set()

# Global application configuration
app_conf = {}


def config():
    app_config = {
        "except_self": True,
        "host": "localhost",
        "port": 8765
    }
    if 'WSS_EXCEPT_SELF' in os.environ:
        app_config["except_self"] = True if os.environ['WSS_EXCEPT_SELF'].lower() == 'true' else False
    if 'WSS_HOST' in os.environ:
        app_config["host"] = os.environ['WSS_HOST']
    if 'WSS_PORT' in os.environ:
        app_config["port"] = os.environ['WSS_PORT']
    return app_config


# Message broadcasting, sends a message to all connected clients
async def broadcast(message, **kwargs):
    clients_copy = clients.copy()

    # If we don`t want to receive our messages - use except_self(bool) argument
    if kwargs["except_self"]:
        clients_copy.remove(kwargs["self_socket"])

    for websocket in clients_copy:
        try:
            await websocket.send(message)
        except websockets.ConnectionClosed:
            clients.remove(websocket)


# Handler for websocket messages
async def handler(websocket, path):
    # Basically, add any client to set of clients
    clients.add(websocket)
    try:
        async for message in websocket:
            await broadcast(message, except_self=app_conf['except_self'], self_socket=websocket)
    # If client disconnects - remove him from set of currently connected clients
    except websockets.exceptions.ConnectionClosedError:
        clients.remove(websocket)


async def main():
    async with websockets.serve(handler, app_conf["host"], app_conf["port"]):
        await asyncio.Future()


if __name__ == '__main__':
    app_conf = config()
    asyncio.run(main())