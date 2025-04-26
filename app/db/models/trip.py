from sqlmodel import Field, SQLModel


class Trip(SQLModel, table=True):
    trip_id: str = Field(primary_key=True, description="Unique identifier for the trip")
    route_id: str = Field(foreign_key="route.route_id",
                          description="Route ID the trip takes")
    service_id: str = Field(foreign_key="calendar.service_id",
                            description="Service ID referencing the calendar")
    trip_headsign: str = Field(description="Text that appears on head signage")
    direction_id: int = Field(description="Direction of travel (1=inbound, 0=outbound)")
    shape_id: str | None = Field(default=None,
                                 description="ID of the shape used for this trip")
