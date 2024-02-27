from threading import Thread
import hashlib
import http.server
import socketserver
import base64

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

def broadcast(msg):
    frame = get_frame(msg)
    for socket in listeners:
        try:
            socket.sendall(frame)
        except OSError as e:
            print(str(e))

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path != '/websocket':
            return super().do_GET()

        listeners.append(self.request)

        self.send_response(101)
        self.send_header("Upgrade", "websocket")
        self.send_header("Connection", "upgrade")
        self.send_header("Sec-WebSocket-Accept", get_accept_header(
            self.headers['Sec-Websocket-Key']
        ))
        self.close_connection = False
        self.end_headers()


def prompt_forever():
    print(PROMPT, end=" ")
    while msg := input():
        broadcast(msg)
        print(">", end=" ")

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    t = Thread(target=prompt_forever)
    t.start()
    with Server(("0.0.0.0", 5000), Handler) as httpd:
        print("serving at port", 5000)
        httpd.serve_forever()
