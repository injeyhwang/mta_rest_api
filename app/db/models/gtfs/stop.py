from sqlmodel import Field, SQLModel


class Stop(SQLModel, table=True):
    stop_id: str = Field(
        primary_key=True,
        description="Unique identifier for the stop")
    stop_name: str = Field(description="Name of the stop")
    stop_lat: float = Field(description="Latitude value of the stop")
    stop_lon: float = Field(description="Longitude value of the stop")
    parent_station: str | None = Field(
        default=None,
        foreign_key="stop.stop_id",
        description=("Stop ID of the parent station. Parent stations contain "
                     "stops for both trip directions"))
