# MTA REST API
A simple REST API reverse proxy for MTA's complicated GTFS and GTFS-RT APIs. Built
with FastAPI and `gtfs-realtime-bindings`

# Static GTFS Files
> Regular GTFS: This file represents the "normal" subway schedule and does not include most temporary service changes, though some long term service changes may be included. It is typically updated a few times a year.

The `/gtfs_subway` directory contains the Regular GTFS Static file downloaded and unzipped from [https://www.mta.info/developers](https://www.mta.info/developers).

The regular GTFS file is downloaded and kept as part of this repository.

**Downloaded date: 04/24/2025**

# Important dependencies
- [FastAPI](https://github.com/fastapi/fastapi)
- [gtfs-realtime-bindings](https://github.com/MobilityData/gtfs-realtime-bindings)

*Note: check `requirements.txt` for list of dependencies*

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
fastapi dev app/main.py
```
*Note: the server runs on port: 8000 so ensure that the port is available.
Otherwise, change the port number.*
