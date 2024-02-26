# Websockets Basics
This is a minimalistic implementatio of a websocket server: /websocket endpoint for
opening a connection with a handshake and a simplest example of sending a correct frame
which consists of at most 126 bytes of text in payload.

Description of the protocol can be found https://datatracker.ietf.org/doc/html/rfc6455.


## Usage
Install the requirements:
`pip install flask requests`

Run the server with:
`py server.py`

Open the client in the web browser under:
`http://<ip>:5000/client.html`

Send messages with server prompt.
You can also inspect the incoming messages in Dev Tools > Networking > /websocket > messages.


## Issues:
werkzeug 3x adds a header "Connection: close" to a response without content-length header.
See the comment `# Always close the connection.` in `werkzeug/serving.py`.
As a workaround we patched `werkzeug.serving`.
