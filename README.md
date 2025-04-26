# MTA REST API
A simple REST API reverse proxy for MTA's complicated GTFS and GTFS-RT APIs. Built
with FastAPI and `gtfs-realtime-bindings`

# Important dependencies
- [FastAPI](https://github.com/fastapi/fastapi)
- [gtfs-realtime-bindings](https://github.com/MobilityData/gtfs-realtime-bindings)
- [SQLModel](https://github.com/fastapi/sqlmodel)

*Note: check `requirements.txt` for list of dependencies*

# Setting up locally
The setup guide will be broken into the following steps:

1. Git clone this repository
2. Download and unzip the latest `gtfs_subway` into the root of this project
3. Set up PostgreSQL database and `mta_admin` user
4. Set up Python and virtual environment
5. Seed the database with the latest `gtfa_subway` data
6. Run `main.py`

## Git clone this repository
Clone this project.
```sh
➜ git clone https://github.com/injeyhwang/mta_rest_api.git
```

## Download the latest regular GTFS static file
> Regular GTFS: This file represents the "normal" subway schedule and does not include most temporary service changes, though some long term service changes may be included. It is typically updated a few times a year.

The `/gtfs_subway` directory at root contains the Regular GTFS Static file downloaded and unzipped from [https://www.mta.info/developers](https://www.mta.info/developers).

Please go to the mta developer website above and download the latest Regular GTFS data into the root of this directory.

**Downloaded date: 04/24/2025**

## Setting up PostgreSQL
### PostgreSQL
I'm on macOS so I will be using homebrew to run postgres. If you're on Windows/Linux or have already set up/know how to configure PostgreSQL for your machine, skip this.

First, install Postgres via homebrew if you haven't already.
```sh
➜ brew install postgresql@16
```

Run postgres via homebrew.
```sh
➜ brew services start postgresql@16
```

To confirm that it's running, you can use the command to confirm that postgres is running.
```sh
➜ brew services list
Name          Status  User File
postgresql@16 started usr  ~/Library/LaunchAgents/homebrew.mxcl.postgresql@16.plist
```

Now let's create our local database. I will call mine `mta_static_db`.
```sh
➜ createdb mta_static_db
```

### Database user: `mta_admin`
Create our admin database user which I'll name `mta_admin`. Give them db privileges.
```sql
-- create this user
CREATE USER mta_admin WITH PASSWORD 'SubwayRatsAreEverywhere';

-- give db privileges
ALTER USER mta_admin WITH CREATEDB;
ALTER USER mta_admin WITH CREATEROLE;
ALTER USER mta_admin WITH LOGIN;

-- schema specific privileges
GRANT ALL PRIVILEGES ON SCHEMA public TO mta_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mta_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mta_admin;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO mta_admin;

-- apply privileges to future objects too
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO mta_admin;
```

## Setting up Python and Virtual Environment
### Python 3
I'm on Apple Silicon and have Python set up via homebrew. If you want your set up to be like mine, install Python via brew. Otherwise, feel free to skip this step.
```sh
brew install python@3.13
```

Add PATH to your `.zshrc`.
```sh
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
```

Verify your installations; you should be able to see the following (Apple Silicon):
```sh
➜ python3 --version
Python 3.13.3

➜ which python3
/opt/homebrew/bin/python3
```

### Virtual Environment
If you haven't done so, please change current working directory to the project root directory. Then create a python virtual environment.

```sh
➜ python3 -m venv .venv
➜ source .venv/bin/activate
```

Install project dependencies with `pip`:
```sh
➜ pip3 install -r requirements.txt
```

## Seed the database with the latest `gtfa_subway` data
At this point, you should have everything set up for the seeding script to work. If you're getting
error messages, take a look at the messages and retrace your steps on this guide.

If all set up accordingly, you should be able to run the seeding script.
```sh
➜ python3 -m scripts.seed_gtfs_static
```

Now check your `mta_static_db` and it should be populated with all the GTFS data!

## Run FastAPI locally
Finally, run the server.

```sh
➜ fastapi dev app/main.py
```
*Note: the server runs on port: 8000 by default. Change the port number by passing the `--port` flag.*

On your browser, go to [http://localhost:8000/docs/](http://localhost:8000/docs/).

You should see all the available endpoints! You can even try them out yourself on the doc page!
