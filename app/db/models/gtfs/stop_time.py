from sqlmodel import Field, SQLModel


class StopTime(SQLModel, table=True):
    trip_id: str = Field(
        primary_key=True,
        foreign_key="trip.trip_id",
        description="Trip ID")
    stop_sequence: int = Field(
        primary_key=True,
        description="Order of stops in the trip")
    stop_id: str = Field(foreign_key="stop.stop_id", description="Stop ID")
    arrival_time: str = Field(description="Arrival time at the stop")
    departure_time: str = Field(description="Departure time from the stop")
