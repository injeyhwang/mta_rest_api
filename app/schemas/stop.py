from pydantic import BaseModel, Field


class StopResponse(BaseModel):
    id: str = Field(description="Unique identifier for the stop")
    name: str = Field(description="Name of the stop")
    latitude: float = Field(description="Latitude value of the stop")
    longitude: float = Field(description="Longitude value of the stop")
