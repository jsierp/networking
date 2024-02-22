Clients initiates websocket connection with GET: /websocket.

Run Server with:
`py server.py`

Open the client in the web browser under:
`http://<ip>:5000/client.html`

Send messages with server prompt.
You can also inspect the incoming messages in Dev Tools > Networking > /websocket > messages.


Issues:
werkzeug 3x adds a header "Connection: close" to a response without content-length header.
As a workaround we pathed werkzeug.serving.