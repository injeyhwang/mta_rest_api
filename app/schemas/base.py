from enum import Enum
from pydantic import BaseModel, Field


class DirectionID(int, Enum):
    INBOUND = 1
    OUTBOUND = 0


class ServiceID(str, Enum):
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"
    WEEKDAY = "Weekday"


class RouteResponse(BaseModel):
    route_id: str = Field(description="Unique identifier for the route")
    route_short_name: str = Field(description="Short name of the route")
    route_long_name: str = Field(description="Full name of the route")
    route_desc: str = Field(description="Description of the route")
    route_url: str = Field(description="URL of the route")
    route_color: str | None = Field(default=None, description="Color of the route in hexadecimal")
    route_text_color: str | None = Field(default=None, description="Text color of the route in hexadecimal")


class TripResponse(BaseModel):
    trip_id: str = Field(description="Unique identifier for the trip")
    route_id: str = Field(description="Route ID the trip takes")
    service_id: ServiceID = Field(description="Service ID referencing the calendar")
    trip_headsign: str = Field(description="Text that appears on head signage")
    direction_id: DirectionID = Field(description="Direction of travel (1=inbound, 0=outbound)")
