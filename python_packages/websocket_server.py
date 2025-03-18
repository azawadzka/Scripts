"""
Websockets
- full-duplex, low-latency communication protocol
- instantly update without you refreshing the page
- persistent connection, real-time, two-way communication
- a single TCP connection
- init: handshake over HTTP -> 101 Switching Protocols -> websockets
- WebSocket frame has a small overhead (~2-14 bytes) compared to an HTTP request (~700-800 bytes)
- stateful
- uses: collaborative editing, multiplayer games, real-time trading, live sports updates, etc.

Tasks (asyncio) 
- asynchronous operations that run concurrently with the main WebSocket communication
- allow you to perform operations without blocking the main WebSocket communication.

Sources:
GitHub Copilot
https://websockets.readthedocs.io/en/stable/intro/examples.html#start-a-server
https://peerlist.io/jagss/articles/websockets-a-deep-dive-into-how-they-work-under-the-hood
"""

import asyncio
import websockets

# A set to keep track of connected clients
connected_clients = set()

async def echo_chatbot(websocket):
    # Register the new client
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Echo the received message to all connected clients
            for client in connected_clients:
                if client != websocket:  # Avoid echoing back to the sender
                    await client.send(f"Client says: {message}")
    except websockets.ConnectionClosed:
        print("A client disconnected.")
    finally:
        # Unregister the client
        connected_clients.remove(websocket)

async def main():
    # Start the WebSocket server
    async with websockets.serve(echo_chatbot, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
