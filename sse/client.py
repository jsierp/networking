import requests

MSG = "Waiting for events.."
print(MSG)
headers = {'Accept': 'text/event-stream'}
headers = {}
event_source = requests.get("http://localhost:5000/events", stream=True, headers=headers)


# The reponse from the server may not be in one chunk, it should be concatenated if so
for event in event_source:
    print(event.decode())
