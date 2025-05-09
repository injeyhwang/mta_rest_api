from sqlmodel import Field, SQLModel


class Shape(SQLModel, table=True):
    shape_id: str = Field(primary_key=True, description="Unique identifier for the shape")
    shape_pt_sequence: int = Field(primary_key=True, description="Sequence of points in the shape")
    shape_pt_lat: float = Field(description="Latitude of shape point")
    shape_pt_lon: float = Field(description="Longitude of shape point")
