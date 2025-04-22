# MTA REST API
A simple REST API reverse proxy for MTA's complicated GTFS and GTFS-RT APIs. Built
with FastAPI and `gtfs-realtime-bindings`

# Setting up locally
First, create then activate virtual environment:

```sh
$ python -m venv .venv
$ source .venv/bin/activate
```

Second, install project dependencies:
```sh
pip install -r requirements.txt
```

Finally, simply run the server by running:

```sh
python -m app.main
```
*Note: the server runs on port: 8000 so ensure that the port is available.
Otherwise, change the port number.*
