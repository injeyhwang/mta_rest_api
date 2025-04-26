from sqlmodel import Field, SQLModel


class Calendar(SQLModel, table=True):
    service_id: str = Field(primary_key=True, description="Unique identifier for the service")
    monday: bool = Field(description="Service operates on Mondays")
    tuesday: bool = Field(description="Service operates on Tuesdays")
    wednesday: bool = Field(description="Service operates on Wednesdays")
    thursday: bool = Field(description="Service operates on Thursdays")
    friday: bool = Field(description="Service operates on Fridays")
    saturday: bool = Field(description="Service operates on Saturdays")
    sunday: bool = Field(description="Service operates on Sundays")
    start_date: str = Field(description="Start date of service in YYYYMMDD format")
    end_date: str = Field(description="End date of service in YYYYMMDD format")


class Route(SQLModel, table=True):
    route_id: str = Field(primary_key=True, description="Unique identifier for the route")
    route_short_name: str = Field(description="Short name of the route")
    route_long_name: str = Field(description="Full name of the route")
    route_desc: str = Field(description="Description of the route")
    route_url: str = Field(description="URL of the route")
    route_color: str | None = Field(default=None, description="Color of the route in hexadecimal")
    route_text_color: str | None = Field(default=None, description="Text color of the route in hexadecimal")


class Shape(SQLModel, table=True):
    shape_id: str = Field(primary_key=True, description="Unique identifier for the shape")
    shape_pt_sequence: int = Field(primary_key=True, description="Sequence of points in the shape")
    shape_pt_lat: float = Field(description="Latitude of shape point")
    shape_pt_lon: float = Field(description="Longitude of shape point")


class StopTime(SQLModel, table=True):
    trip_id: str = Field(primary_key=True, foreign_key="trip.trip_id", description="Trip ID")
    stop_sequence: int = Field(primary_key=True, description="Order of stops in the trip")
    stop_id: str = Field(foreign_key="stop.stop_id", description="Stop ID")
    arrival_time: str = Field(description="Arrival time at the stop")
    departure_time: str = Field(description="Departure time from the stop")


class Stop(SQLModel, table=True):
    stop_id: str = Field(primary_key=True, index=True, description="Unique identifier for the stop")
    stop_name: str = Field(description="Name of the stop")
    stop_lat: float = Field(description="Latitude value of the stop")
    stop_lon: float = Field(description="Longitude value of the stop")
    parent_station: str | None = Field(default=None,
                                       foreign_key="stop.stop_id",
                                       description="Stop ID of the parent station. Parent stations \
                                           contain stops for both trip directions")


class Transfer(SQLModel, table=True):
    from_stop_id: str = Field(primary_key=True, foreign_key="stop.stop_id",
                              description="Stop ID where transfer begins")
    to_stop_id: str = Field(primary_key=True,
                            foreign_key="stop.stop_id",
                            description="Stop ID where transfer ends")
    transfer_type: int = Field(description="Type of transfer (0=recommended, 1=timed, 2=min_time, 3=not_possible)")
    min_transfer_time: int | None = Field(default=None,
                                          description="Minimum time required for transfer in seconds")


class Trip(SQLModel, table=True):
    trip_id: str = Field(primary_key=True, description="Unique identifier for the trip")
    route_id: str = Field(foreign_key="route.route_id",
                          description="Route ID the trip takes")
    service_id: str = Field(foreign_key="calendar.service_id",
                            description="Service ID referencing the calendar")
    trip_headsign: str = Field(description="Text that appears on head signage")
    direction_id: int = Field(description="Direction of travel (1=inbound, 0=outbound)")
    shape_id: str | None = Field(default=None,
                                 description="ID of the shape used for this trip")
