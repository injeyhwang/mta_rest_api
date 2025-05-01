from pydantic import BaseModel, Field


class RouteResponse(BaseModel):
    id: str = Field(description="Unique identifier for the route")
    short_name: str = Field(description="Short name of the route")
    long_name: str = Field(description="Full name of the route")
    description: str = Field(description="Description of the route")
    url: str = Field(description="URL of the route")
    color: str | None = Field(default=None, description="Color of the route in hexadecimal")
    text_color: str | None = Field(default=None, description="Text color of the route in hexadecimal")
