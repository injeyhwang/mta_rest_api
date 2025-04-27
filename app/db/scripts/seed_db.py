import csv
from datetime import datetime
import os
from sqlmodel import select, Session
from typing import Any, Dict, List

# SQLModel is imported from app.db.database because Python executes all the code creating the classes
# inheriting from SQLModel and registering them in the SQLModel.metadata.
#
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata-order-matters
from app.db.database import get_db_engine, SQLModel
from app.db.models import Calendar, Route, Stop, Shape, StopTime, Transfer, Trip
from app.db.scripts.init_db import create_db_tables
from app.utils.logger import logger


GTFS_DIR_PATH = os.environ.get("GTFS_DIR_PATH")


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    records = []

    logger.info(f"Reading CSV file: '{file_path}'")
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [name.lower() for name in reader.fieldnames]

        for row in reader:
            records.append({ key: value for (key, value) in row.items() })

    logger.info(f"Successfully read {len(records)} records from '{file_path}'")
    return records


def convert_field_types(data: List[Dict[str, Any]], model_class: SQLModel) -> List[Dict[str, Any]]:
    converted_data = []
    for record in data:
        converted_record = {}
        for field, value in record.items():
            # skip if value is empty
            if value is None or value == "":
                continue

            # convert types based on model field types
            model_field = model_class.model_fields.get(field)
            if model_field is not None:
                field_type = model_field.annotation
                if field_type == bool:
                    # Convert '0'/'1' strings to actual boolean values
                    converted_record[field] = value == '1'
                elif field_type == float:
                    try:
                        converted_record[field] = float(value)
                    except ValueError:
                        logger.exception(f"Could not convert '{value}' to float for field '{field}'")
                elif field_type == int:
                    try:
                        converted_record[field] = int(value)
                    except ValueError:
                        logger.exception(f"Could not convert '{value}' to int for field '{field}'")
                else:
                    # keep as string for other data types
                    converted_record[field] = value
            else:
                # field is not defined in model and so can't convert - keep it as is
                converted_record[field] = value

        converted_data.append(converted_record)

    return converted_data


def seed_routes(session: Session):
    try:
        routes_file_path = os.path.join(GTFS_DIR_PATH, "routes.txt")
        if not os.path.exists(routes_file_path):
            raise FileNotFoundError(f"Routes file not found at: '{routes_file_path}'")

        routes_data = read_csv_file(routes_file_path)
        routes_data = convert_field_types(routes_data, Route)

        for route_dict in routes_data:
            route = Route(**route_dict)
            session.add(route)

        logger.info(f"Adding {len(routes_data)} entries to the routes table")
        session.commit()
        logger.info("Successfully committed routes to database")
    except Exception as e:
        logger.exception(f"Error seeding routes: {e}")
        session.rollback()
        logger.info("Routes changes rolled back")
        raise


def seed_stops(session: Session):
    try:
        stops_file_path = os.path.join(GTFS_DIR_PATH, "stops.txt")
        if not os.path.exists(stops_file_path):
            raise FileNotFoundError(f"Stops file not found at: '{stops_file_path}'")

        stops_data = read_csv_file(stops_file_path)
        stops_data = convert_field_types(stops_data, Stop)

        # first pass: add all stops without parent_station to avoid foreign key constraints
        for stop_dict in stops_data:
            if stop_dict.get('parent_station') is None:
                stop = Stop(**stop_dict)
                session.add(stop)

        # second pass: add stops with parent_station
        for stop_dict in stops_data:
            if stop_dict.get('parent_station') is not None:
                statement = select(Stop).where(Stop.stop_id == stop_dict['stop_id'])
                existing_stop = session.exec(statement).first()
                if not existing_stop:
                    stop = Stop(**stop_dict)
                    session.add(stop)

        logger.info(f"Adding {len(stops_data)} entries to the stop table")
        session.commit()
        logger.info("Successfully committed stops to database")
    except Exception as e:
        logger.exception(f"Error seeding stops: {e}")
        session.rollback()
        logger.info("Stops changes rolled back")
        raise


def seed_calendar(session: Session):
    try:
        calendar_file_path = os.path.join(GTFS_DIR_PATH, "calendar.txt")
        if not os.path.exists(calendar_file_path):
            raise FileNotFoundError(f"Calendar file not found at: '{calendar_file_path}'")

        calendar_data = read_csv_file(calendar_file_path)
        calendar_data = convert_field_types(calendar_data, Calendar)

        for calendar_dict in calendar_data:
            calendar = Calendar(**calendar_dict)
            session.add(calendar)

        logger.info(f"Adding {len(calendar_data)} entries to the calendar table")
        session.commit()
        logger.info("Successfully committed calendar entries to database")
    except Exception as e:
        logger.exception(f"Error seeding calendar: {e}")
        session.rollback()
        logger.info("Calendar changes rolled back")
        raise


def seed_shapes(session: Session):
    try:
        shapes_file_path = os.path.join(GTFS_DIR_PATH, "shapes.txt")
        if not os.path.exists(shapes_file_path):
            raise FileNotFoundError(f"Shapes file not found: {shapes_file_path}")

        shapes_data = read_csv_file(shapes_file_path)
        shapes_data = convert_field_types(shapes_data, Shape)

        for shape_dict in shapes_data:
            shape = Shape(**shape_dict)
            session.add(shape)

        logger.info(f"Adding {len(shapes_data)} entries to the shape table")
        session.commit()
        logger.info("Successfully committed shapes to database")
    except Exception as e:
        logger.exception(f"Error seeding shapes: {e}")
        session.rollback()
        logger.info("Shapes changes rolled back")
        raise


def seed_trips(session: Session):
    try:
        trips_file_path = os.path.join(GTFS_DIR_PATH, "trips.txt")
        if not os.path.exists(trips_file_path):
            raise FileNotFoundError(f"Trips file not found: '{trips_file_path}'")

        trips_data = read_csv_file(trips_file_path)
        trips_data = convert_field_types(trips_data, Trip)

        for trip_dict in trips_data:
            trip = Trip(**trip_dict)
            session.add(trip)

        logger.info(f"Adding {len(trips_data)} entries to the trip table")
        session.commit()
        logger.info("Successfully committed trips to database")
    except Exception as e:
        logger.exception(f"Error seeding trips: {e}")
        session.rollback()
        logger.info("Trips changes rolled back")
        raise


def seed_stop_times(session: Session):
    try:
        stop_times_file_path = os.path.join(GTFS_DIR_PATH, "stop_times.txt")
        if not os.path.exists(stop_times_file_path):
            raise FileNotFoundError(f"Stop times file not found: '{stop_times_file_path}'")

        def _process_stop_times_batch(session: Session, batch_records: List[Dict[str, Any]]):
            stop_times_data = convert_field_types(batch_records, StopTime)
            for stop_time_dict in stop_times_data:
                stop_time = StopTime(**stop_time_dict)
                session.add(stop_time)

        # Process stop_times in batches
        batch_size = 10000
        total_records = 0

        with open(stop_times_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch_records = []
            for row in reader:
                total_records += 1
                batch_records.append(row)

                if len(batch_records) >= batch_size:
                    _process_stop_times_batch(session, batch_records)
                    logger.info(f"Processed {total_records} stop times")
                    batch_records = []

            # Process remaining records
            if batch_records:
                _process_stop_times_batch(session, batch_records)

        logger.info(f"Adding a total of {total_records} entries to the stop_times table")
        session.commit()
        logger.info("Successfully committed stop times to database")
    except Exception as e:
        logger.exception(f"Error seeding stop times: {e}")
        session.rollback()
        logger.info("Stop times changes rolled back")
        raise


def seed_transfers(session: Session):
    try:
        transfers_file_path = os.path.join(GTFS_DIR_PATH, "transfers.txt")
        if not os.path.exists(transfers_file_path):
            raise FileNotFoundError(f"Transfers file not found: '{transfers_file_path}'")

        transfers_data = read_csv_file(transfers_file_path)
        transfers_data = convert_field_types(transfers_data, Transfer)

        for transfer_dict in transfers_data:
            transfer = Transfer(**transfer_dict)
            session.add(transfer)

        logger.info(f"Adding {len(transfers_data)} entries to the transfer table")
        session.commit()
        logger.info("Successfully committed transfers to database")
    except Exception as e:
        logger.exception(f"Error seeding transfers: {e}")
        session.rollback()
        logger.info("Transfers changes rolled back")
        raise


def seed_database():
    """
    Seed the database with GTFS static data.
    """
    start_time = datetime.now()
    logger.info(f"Starting GTFS data seeding at {start_time}")

    if not os.path.exists(GTFS_DIR_PATH):
        logger.error(f"GTFS directory not found at: '{GTFS_DIR_PATH}'")
        return

    try:
        # Initialize database and tables if they don't exist; get engine to perform database seeding
        engine = get_db_engine()
        create_db_tables(engine)

        with Session(engine) as session:
            # Seed tables in order of dependencies
            seed_routes(session)
            seed_stops(session)
            seed_calendar(session)
            seed_shapes(session)
            seed_trips(session)
            seed_stop_times(session)
            seed_transfers(session)

            end_time = datetime.now()
            duration = end_time - start_time
            logger.info(f"Database seeding completed successfully in {duration}")
    finally:
        if engine:
            logger.info("Disposing database engine")
            engine.dispose()
            logger.info("Database connections closed")


if __name__ == "__main__":
    seed_database()
