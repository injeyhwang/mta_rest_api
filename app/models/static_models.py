from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class Route(BaseModel):
    route_id: str = Field(description="Unique identifier for the route")
    route_short_name: str = Field(description="Short name of the route")
    route_long_name: str = Field(description="Full name of the route")
    route_desc: str = Field(description="Description of the route")
    route_url: str = Field(description="URL of the route")
    route_color: Optional[str] = Field(default=None,
                                       description="Color of the route in hexadecimal")
    route_text_color: Optional[str] = Field(default=None,
                                            description="Text color of the route in hexadecimal")


class Stop(BaseModel):
    stop_id: str = Field(description="Unique identifier for the stop")
    stop_name: str = Field(description="Name of the stop")
    stop_lat: float = Field(description="Latitude value of the stop")
    stop_lon: float = Field(description="Longitude value of the stop")
    parent_station: Optional[str] = Field(default=None, description="Stop ID of the parent station. \
        Parent stations contain stops for both trip directions")


class Service(str, Enum):
    WEEKDAY = "Weekday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class Direction(int, Enum):
    IN_BOUND = 1
    OUT_BOUND = 0


class Trip(BaseModel):
    trip_id: str = Field(description="Unique identifier for the trip")
    route_id: str = Field(description="Unique identifier of the route the trip takes")
    service_id: Service = Field(description="Subway service ID consisting of 'Weekday', \
        'Saturday', or 'Sunday'")
    trip_headsign: str = Field(default=None, description="Text that appears on signage")
    direction_id: Direction = Field(description="Direction of travel. This differs per route, but \
        typically 1 for inbound and 0 for outbound to/from the city")


class StopTime(BaseModel):
    trip_id: str = Field(description="Trip ID")
    stop_id: str = Field(description="Stop ID")
    arrival_time: str = Field(description="Arrival time at the stop")
    departure_time: str = Field(description="Departure time from the stop")
    stop_sequence: int = Field(description="Order of stops in the trip")
