from pydantic import BaseModel, Field
from typing import List

from app.schemas.trip import TripResponse


class StopTimeResponse(BaseModel):
    trip: TripResponse = Field(description="Trip that the stop time belongs to")
    stop_sequence: int = Field(description="Order of stops in the trip")
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
