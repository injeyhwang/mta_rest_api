from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class DirectionID(int, Enum):
    """
    1 is mapped to stop_ids ending with N.
    0 is mapped to stop_ids ending with S.
    """
    INBOUND = 1
    OUTBOUND = 0


class ServiceID(str, Enum):
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"
    WEEKDAY = "Weekday"


class ScheduledStop(BaseModel):
    id: str = Field(description="Unique identifier for the stop")
    name: str = Field(description="Name of the stop")
    latitude: float = Field(description="Latitude value of the stop")
    longitude: float = Field(description="Longitude value of the stop")


class TripSchedule(BaseModel):
    stop: ScheduledStop = Field(description="Stop of this stop time")
    stop_sequence: int = Field(description="Order of stops in the trip")
    arrival_time: str = Field(description="Arrival time at the stop")
    departure_time: str = Field(description="Departure time from the stop")


class TripSimple(BaseModel):
    id: str = Field(description="Unique identifier for the trip")
    headsign: str = Field(description="Text that appears on head signage")
    route_id: str = Field(description="Route ID the trip takes")
    service_id: ServiceID = Field(
        description="Service ID referencing the calendar")
    direction_id: DirectionID = Field(
        description="Direction of travel (1=inbound, 0=outbound)")


class TripDetailed(BaseModel):
    id: str = Field(description="Unique identifier for the trip")
    headsign: str = Field(description="Text that appears on head signage")
    route_id: str = Field(description="Route ID the trip takes")
    service_id: ServiceID = Field(
        description="Service ID referencing the calendar")
    direction_id: DirectionID = Field(
        description="Direction of travel (1=inbound, 0=outbound)")
    stop_times: List[TripSchedule] = Field(
        description="Scheduled stop times on this trip")
