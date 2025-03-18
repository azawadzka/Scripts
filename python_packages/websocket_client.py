import asyncio
import websockets

async def chat_client():
    uri = "ws://localhost:8765"  # Server address
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to the server. Type your messages below:")
            
            async def send_messages():
                while True:
                    message = await asyncio.to_thread(input, "You: ")
                    await websocket.send(message)
                    print(f"Sent to server: {message}")

            async def receive_messages():
                while True:
                    response = await websocket.recv()
                    print(f"Server: {response}")

            # Run send and receive tasks concurrently
            send_task = asyncio.create_task(send_messages())
            receive_task = asyncio.create_task(receive_messages())
            await asyncio.gather(send_task, receive_task)
    except (websockets.ConnectionClosed, ConnectionRefusedError):
        print("Connection to the server was closed or refused.")

if __name__ == "__main__":
    asyncio.run(chat_client())