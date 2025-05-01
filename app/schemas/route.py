from pydantic import BaseModel, Field


class RouteResponse(BaseModel):
    route_id: str = Field(description="Unique identifier for the route")
    route_short_name: str = Field(description="Short name of the route")
    route_long_name: str = Field(description="Full name of the route")
    route_desc: str = Field(description="Description of the route")
    route_url: str = Field(description="URL of the route")
    route_color: str | None = Field(default=None, description="Color of the route in hexadecimal")
    route_text_color: str | None = Field(default=None, description="Text color of the route in hexadecimal")
