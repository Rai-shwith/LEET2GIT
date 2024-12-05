import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

# Serve the frontend HTML
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Step Process</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        input, button { padding: 10px; margin-right: 10px; }
        button { cursor: pointer; }
        .message { margin-top: 10px; padding: 10px; background-color: #f9f9f9; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>WebSocket Step Process Example</h1>
    <div>
        <input type="text" id="userInput" placeholder="Enter some data..." />
        <button onclick="sendMessage()">Send</button>
    </div>
    <div id="messages"></div>

    <script>
        // Establish WebSocket connection
        const socket = new WebSocket("ws://localhost:8000/ws");

        socket.onopen = () => {
            console.log("WebSocket connection established.");
        };

        socket.onmessage = (event) => {
            // Display the server's response
            const messageDiv = document.createElement("div");
            messageDiv.className = "message";
            messageDiv.textContent = "Server: " + event.data;
            document.getElementById("messages").appendChild(messageDiv);
        };

        socket.onclose = () => {
            console.log("WebSocket connection closed.");
        };

        socket.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        // Send a message to the server
        function sendMessage() {
            const input = document.getElementById("userInput");
            const message = input.value.trim();
            if (message) {
                socket.send(message);
                const messageDiv = document.createElement("div");
                messageDiv.className = "message";
                messageDiv.textContent = "You: " + message;
                document.getElementById("messages").appendChild(messageDiv);
                input.value = ""; // Clear the input field
            }
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept the WebSocket connection
    try:
        while True:
            # Receive a message from the client
            data = await websocket.receive_text()
            print(f"Message received from client: {data}")

            # Process Step 1
            await asyncio.sleep(2)  # Simulate time-consuming task
            await websocket.send_text("Step 1 completed: Validating data...")

            # Process Step 2
            await asyncio.sleep(3)  # Simulate time-consuming task
            await websocket.send_text("Step 2 completed: Processing data...")

            # Process Step 3
            await asyncio.sleep(2)  # Simulate time-consuming task
            await websocket.send_text("Step 3 completed: Finalizing response...")

            # Final response
            await websocket.send_text(f"All steps completed! Processed data: {data.upper()}")
    except WebSocketDisconnect:
        print("Client disconnected")
