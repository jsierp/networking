Clients requests event source with GET: /events.

Run Server with:
`py sse/server.py 2>/dev/null`

Run client:
`py sse/client.py`


In a web browser you would use:
`
const evtSource = new EventSource("localhost:5000/events");

evtSource.onmessage = (event) => {
    console.log(event.event);
    console.log(event.data);
};
`