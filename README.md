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

1. Set up Python and virtual environment
2. Set up PostgreSQL database and `mta_admin` user
3. [Optional] Download and unzip the latest `gtfs_subway`
4. Initialize and seed the database
5. Run `main.py`

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

## [Optional] Download the latest regular GTFS static file
If you'd like to use the latest regular GTFS Static data, you can go to [https://www.mta.info/developers](https://www.mta.info/developers) and download, unzip, and replace the `gtfs_subway` file into `app/db/` directory.

> Regular GTFS: This file represents the "normal" subway schedule and does not include most temporary service changes, though some long term service changes may be included. It is typically updated a few times a year.

**Regular GTFS Static downloaded date: 04/24/2025**

## Initialize and seed the database
At this point, you should have everything set up for the database scripts to work. If you're getting
any error messages, take a look at them and debug by retrace your steps on this guide.

If all set up accordingly, you should be able to run the db scripts.
```sh
➜ python3 -m app.db.scripts.init_db

➜ python3 -m app.db.scripts.seed_db
```

Now check your `mta_static_db` and it should be populated with all the GTFS data!

If in the future you'd like to reset the database with the latest data, you can use the `reset_db`
script to drop everything from the database and initialize the database with tables. You could then
run the seeding script to import over the latest GTFS static data.
```sh
➜ python3 -m app.db.scripts.reset_db

➜ python3 -m app.db.scripts.seed_db
```

## Run FastAPI locally
Finally, run the server.

```sh
➜ fastapi dev app/main.py
```
*Note: the server runs on port: 8000 by default. Change the port number by passing the `--port` flag.*

On your browser, go to [http://localhost:8000/docs/](http://localhost:8000/docs/).

You should see all the available endpoints! You can even try them out yourself on the doc page!
