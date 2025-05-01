from enum import Enum
from pydantic import BaseModel, Field


class DirectionID(int, Enum):
    INBOUND = 1
    OUTBOUND = 0


class ServiceID(str, Enum):
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"
    WEEKDAY = "Weekday"


class TripResponse(BaseModel):
    id: str = Field(description="Unique identifier for the trip")
    headsign: str = Field(description="Text that appears on head signage")
    route_id: str = Field(description="Route ID the trip takes")
    service_id: ServiceID = Field(description="Service ID referencing the calendar")
    direction_id: DirectionID = Field(description="Direction of travel (1=inbound, 0=outbound)")
