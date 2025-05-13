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


class EntityType(str, Enum):
    ALERT = "alert"
    TRIP_UPDATE = "trip_schedule_update"
    VEHICLE = "vehicle_position"


class VehicleStatus(str, Enum):
    """
    Current status of a transit vehicle relative to stops.

    These statuses describe the vehicle's relationship to the stop
    sequence along its route.
    """
    INCOMING_AT = "INCOMING_AT"      # Vehicle is approaching a stop
    STOPPED_AT = "STOPPED_AT"        # Vehicle is at a stop
    IN_TRANSIT_TO = "IN_TRANSIT_TO"  # Vehicle has departed previous stop


class TimeData(BaseModel):
    """
    Timing information for arrivals and departures.

    Contains Unix timestamps representing when a vehicle is predicted
    to arrive at or depart from a stop.
    """
    time: str = Field(
        description="Unix timestamp (seconds since epoch) for the event")


class StopTimeUpdateData(BaseModel):
    """
    Real-time update for a single stop in a trip.

    Provides predicted arrival/departure times for a vehicle at a
    specific stop, including its relationship to the schedule.
    """
    stop_id: str | None = Field(
        default=None,  # remove
        description="GTFS stop_id where the prediction applies")
    arrival: TimeData | None = Field(
        default=None,
        description="Predicted arrival time at this stop")
    departure: TimeData | None = Field(
        default=None,
        description="Predicted departure time from this stop")


class TripData(BaseModel):
    """
    Identifies a trip instance in GTFS-RT.

    Contains the necessary fields to uniquely identify a trip and match
    it to the static GTFS schedule data.
    """
    trip_id: str = Field(
        description="Unique identifier matching GTFS trips.txt trip_id")
    route_id: str = Field(
        description="Route identifier matching GTFS routes.txt route_id")
    start_time: str | None = Field(
        default=None,
        description="Scheduled trip start time in HH:MM:SS format")
    start_date: str | None = Field(
        default=None,
        description="Service date for the trip in YYYYMMDD format")


class InformedEntity(BaseModel):
    trip: TripData = Field("Alerted trips")


class HeaderText(BaseModel):
    text: str = Field("Description of the alert")


class AlertHeaderData(BaseModel):
    translation: List[HeaderText] = Field(
        description="List of translated header text")


class AlertData(BaseModel):
    """
    Real-time feed alert information for a specific feed.

    Lists impacted trips for this alert.
    """
    header_text: AlertHeaderData = Field(description="")
    informed_entity: List[InformedEntity] = Field(
        default=[],
        description="List of trips alerted")


class TripUpdateData(BaseModel):
    """
    Real-time trip update information for a specific feed.

    Contains predictions for arrival and departure times at stops along
    a trip's route, representing deviations from the static schedule.
    """
    trip: TripData = Field(
        description="Trip identifier for these updates")
    stop_time_update: List[StopTimeUpdateData] = Field(
        default=[],
        description="Predicted times for stops along this trip")


class VehicleData(BaseModel):
    """
    Real-time position information for a transit vehicle.

    Describes the current location and status of a vehicle on its route,
    including which trip it's serving and its position in the stop sequence.
    """
    trip: TripData = Field(
        description="Trip that this vehicle is currently serving")
    timestamp: str = Field(
        description="Unix timestamp when this position was recorded")
    stop_id: str = Field(
        description="Nearest stop to the vehicle's current position")
    current_stop_sequence: int | None = Field(
        default=None,
        description="Index of current stop in the trip's stop sequence")
    current_status: VehicleStatus | None = Field(
        default=None,
        description="Vehicle's status relative to the current stop")


class FeedResponseHeader(BaseModel):
    """
    Metadata header for GTFS-RT feed messages.

    Contains version information and timestamp for the feed update,
    allowing consumers to track feed freshness and compatibility.
    """
    gtfs_realtime_version: str = Field(
        description="GTFS-RT specification version (e.g., '1.0', '2.0')")
    timestamp: str = Field(
        description="Unix timestamp when this feed update was generated")


class Entity(BaseModel):
    """
    Generic entity that can contain trip updates, vehicle positions, or alerts.

    In GTFS-RT, each entity in the feed must contain exactly one of:
    trip_update, vehicle, or alert. This implementation supports
    trip_update and vehicle entities.
    """
    id: str = Field(
        description="Unique identifier for this entity in the feed")
    alert: AlertData | None = Field(
        default=None,
        description="Real-time alert information")
    trip_update: TripUpdateData | None = Field(
        default=None,
        description="Real-time trip schedule update information")
    vehicle: VehicleData | None = Field(
        default=None,
        description="Real-time vehicle position information")

    @property
    def entity_type(self) -> EntityType:
        if self.alert is not None:
            return EntityType.ALERT
        elif self.trip_update is not None:
            return EntityType.TRIP_UPDATE
        elif self.vehicle is not None:
            return EntityType.VEHICLE


class FeedResponse(BaseModel):
    """
    Complete GTFS-RT feed message from MTA.

    Root object containing the feed header metadata and a list of
    entities (trip updates and/or vehicle positions) that comprise
    the real-time transit information update.
    """
    header: FeedResponseHeader = Field(
        description="Feed metadata including version and timestamp")
    entity: List[Entity] = Field(
        description="Collection of trip updates and/or vehicle positions")
