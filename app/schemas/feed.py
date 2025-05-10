from enum import Enum
from typing import List

from pydantic import BaseModel, Field


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
    time: str = Field(
        description="Unix timestamp of the arrival/departure time")


class StopTimeUpdate(BaseModel):
    stop_id: str = Field(description="Stop ID")
    arrival: TimeData | None = Field(
        default=None,
        description="Arrival time information")
    departure: TimeData | None = Field(
        default=None,
        description="Departure time information")


class TripData(BaseModel):
    trip_id: str = Field(description="Unique identifier for the trip")
    route_id: str = Field(description="Route ID - e.g. 'A', 'C', 'E', etc...")
    start_time: str | None = Field(
        default=None,
        description="Scheduled start time of the trip - formatted 'HH:MM:SS'")
    start_date: str | None = Field(
        default=None,
        description="Scheduled start date of the trip - formatted 'YYYMMDD'")
    stop_id: str | None = Field(None, description="Current stop ID")


class VehicleData(BaseModel):
    trip: TripData
    timestamp: str = Field(
        description="Unix timestamp of the vehicle position")
    stop_id: str = Field(description="Current stop ID")
    current_stop_sequence: int | None = Field(
        default=None,
        description=("Current vehicle position on the route stop order "
                     "sequence"))
    current_status: VehicleStatus | None = Field(
        default=None,
        description="Current status of the vehicle")


class TripUpdate(BaseModel):
    trip: TripData
    stop_time_update: List[StopTimeUpdate] | None = Field(
        default=None,
        description="List of stop time updates")


class Entity(BaseModel):
    id: str = Field(description="Unique identifier for the entity")
    trip_update: TripUpdate | None = Field(
        default=None,
        description="Real-time trip update information")
    vehicle: VehicleData | None = Field(
        default=None,
        description="Vehicle position information")


class FeedHeader(BaseModel):
    gtfs_realtime_version: str = Field(description="MTA's GTFS-RT API version")
    timestamp: str = Field(description="Unix timestamp of the request")


class FeedDetailed(BaseModel):
    header: FeedHeader = Field(description="GTFS-RT header metadata")
    entity: List[Entity] = Field(description="List of feed entities")
