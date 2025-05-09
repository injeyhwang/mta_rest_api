from pydantic import BaseModel, Field
from typing import List

from app.schemas.trip import ServiceID


class StopTimeTrip(BaseModel):
    id: str = Field(description="Unique identifier for the trip")
    headsign: str = Field(description="Text that appears on head signage")
    route_id: str = Field(description="Route ID the trip takes")
    service_id: ServiceID = Field(description="Service ID referencing the calendar")


class StopTimeResponse(BaseModel):
    trip: StopTimeTrip = Field(description="Trip that the stop time belongs to")
    arrival_time: str = Field(description="Arrival time at the stop")
    departure_time: str = Field(description="Departure time from the stop")


class StopResponse(BaseModel):
    id: str = Field(description="Unique identifier for the stop")
    name: str = Field(description="Name of the stop")
    latitude: float = Field(description="Latitude value of the stop")
    longitude: float = Field(description="Longitude value of the stop")


class StopDetailedResponse(BaseModel):
    id: str = Field(description="Unique identifier for the stop")
    name: str = Field(description="Name of the stop")
    latitude: float = Field(description="Latitude value of the stop")
    longitude: float = Field(description="Longitude value of the stop")
    stop_times: List[StopTimeResponse] = Field(description="Scheduled stop times on this stop")
