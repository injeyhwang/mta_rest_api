from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class Feed(str, Enum):
    ACE = "ACE"
    BDFM = "BDFM"
    G = "G"
    JZ = "JZ"
    NQRW = "NQRW"
    L = "L"
    S1234567 = "S1234567"
    SIR = "SIR"


class VehicleStatus(str, Enum):
    INCOMING_AT = "INCOMING_AT"
    STOPPED_AT = "STOPPED_AT"
    IN_TRANSIT_TO = "IN_TRANSIT_TO"


class TimeData(BaseModel):
    time: str = Field(description="Unix timestamp of the arrival/departure time")


class StopTimeUpdate(BaseModel):
    arrival: Optional[TimeData] = Field(None, description="Arrival time information")
    departure: Optional[TimeData] = Field(None, description="Departure time information")
    stop_id: str = Field(description="Stop ID")


class TripData(BaseModel):
    trip_id: str = Field(description="Unique identifier for the trip")
    start_time: Optional[str] = Field(None, description="Scheduled start time of the trip - formatted 'HH:MM:SS'")
    start_date: Optional[str] = Field(None, description="Scheduled start date of the trip - formatted 'YYYMMDD'")
    route_id: str = Field(description="Route ID - e.g. 'A', 'C', 'E', etc...")
    stop_id: Optional[str] = Field(None, description="Current stop ID")


class VehicleData(BaseModel):
    trip: TripData
    timestamp: str = Field(description="Unix timestamp of the vehicle position")
    stop_id: str = Field(description="Current stop ID")
    current_stop_sequence: Optional[int] = Field(None, description="Current vehicle position on the route stop order sequence")
    current_status: Optional[VehicleStatus] = Field(None, description="Current status of the vehicle")


class TripUpdate(BaseModel):
    trip: TripData
    stop_time_update: Optional[List[StopTimeUpdate]] = Field(None, description="List of stop time updates")


class Entity(BaseModel):
    id: str = Field(description="Unique identifier for the entity")
    trip_update: Optional[TripUpdate] = Field(None, description="Real-time trip update information")
    vehicle: Optional[VehicleData] = Field(None, description="Vehicle position information")


class FeedHeader(BaseModel):
    gtfs_realtime_version: str = Field(description="MTA's GTFS-RT API version")
    timestamp: str = Field(description="Unix timestamp of the request")


class FeedResponse(BaseModel):
    header: FeedHeader
    entity: List[Entity] = Field(description="List of feed entities")
