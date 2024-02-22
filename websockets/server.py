from flask import Flask, Response, request
import queue
from threading import Thread
import hashlib
import base64

app = Flask(__name__, static_url_path="", static_folder=".")

PROMPT = "Waiting for input\n>"

listeners = []

HANDSHAKE_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

def get_accept_header(sec_websocket_key):
    return base64.b64encode(
            hashlib.sha1((
                    sec_websocket_key + HANDSHAKE_GUID
                ).encode()
            ).digest()
        ).decode()

def get_frame(msg):
    msg = msg.encode()
    payload_length = len(msg)
    if payload_length > 125:
        raise Exception("unsupported paylod legth")
    frame = (
        (0b10000001).to_bytes(1, 'big')
        + payload_length.to_bytes(1, 'big')
    ) + msg
    return frame

@app.route("/websocket", websocket=True)
def websocket():
    listeners.append(request.environ['werkzeug.socket'])

    response = Response(status=101, headers={
        'Upgrade': 'websocket',
        'Connection': 'upgrade',
        'Sec-WebSocket-Accept': get_accept_header(
            request.headers['Sec-Websocket-Key']
        ),
    })
    return response

def broadcast(msg):
    frame = get_frame(msg)
    for socket in listeners:
        try:
            socket.sendall(frame)
        except OSError as e:
            print(str(e))

if __name__ == "__main__":
    t = Thread(target=lambda: app.run(host="0.0.0.0"))
    t.start()

    print(PROMPT, end=" ")
    while msg := input():
        broadcast(msg)
        print(">", end=" ")
