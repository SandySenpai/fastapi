from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

# Define a set of keywords for triggering reminders
KEYWORDS = {"remind", "todo", "schedule", "buy"}

# HTML for a simple client interface (for testing purposes)
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>OMI Audio Streaming Test</title>
    </head>
    <body>
        <h1>WebSocket Test for Audio Streaming</h1>
        <textarea id="log" rows="20" cols="50"></textarea><br/>
        <input type="text" id="messageInput" placeholder="Type a message..."/>
        <button onclick="sendMessage()">Send</button>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                const log = document.getElementById("log");
                log.value += event.data + "\\n";
            };
            function sendMessage() {
                const input = document.getElementById("messageInput");
                ws.send(input.value);
                input.value = "";
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
    await websocket.accept()
    try:
        while True:
            # In a real scenario, OMI would send continuous audio transcription text.
            data = await websocket.receive_text()
            print("Received:", data)
            # Process the text for any keyword
            found_keywords = [kw for kw in KEYWORDS if kw in data.lower()]
            if found_keywords:
                reminder_message = f"Reminder: Detected keywords - {', '.join(found_keywords)}"
                # Send back a reminder
                await websocket.send_text(reminder_message)
            else:
                await websocket.send_text("No reminder triggered.")
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
