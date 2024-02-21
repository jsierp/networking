from flask import Flask, Response
import queue
from threading import Thread

app = Flask(__name__, )

PROMPT = "Waiting for input\n>"

listeners = []

@app.route("/events", methods=["GET"])
def listen():
    def stream():
        listeners.append(messages := queue.Queue(maxsize=100))
        while True:
            msg = messages.get()
            yield msg
    response = Response(stream(), mimetype="text/event-stream")
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response 

def broadcast(msg):
    for q in listeners:
        q.put(msg)

if __name__ == "__main__":
    t = Thread(target=app.run)
    t.start()

    print(PROMPT, end=" ")
    while msg := input():
        broadcast(f"event: message\ndata:{msg}\n\n")
        print(">", end=" ")