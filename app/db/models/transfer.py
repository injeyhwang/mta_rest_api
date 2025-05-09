from sqlmodel import Field, SQLModel


class Transfer(SQLModel, table=True):
    from_stop_id: str = Field(primary_key=True, foreign_key="stop.stop_id",
                              description="Stop ID where transfer begins")
    to_stop_id: str = Field(primary_key=True,
                            foreign_key="stop.stop_id",
                            description="Stop ID where transfer ends")
    transfer_type: int = Field(description="Type of transfer (0=recommended, 1=timed, 2=min_time, 3=not_possible)")
    min_transfer_time: int | None = Field(default=None,
                                          description="Minimum time required for transfer in seconds")
