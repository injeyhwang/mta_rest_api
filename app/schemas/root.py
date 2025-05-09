from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    app_name: str = Field(description="App name")
    app_version: str = Field(description="App version")
    app_description: str = Field(description="App description")
    api_version: str = Field(description="Latest API version")
    documentation_url: str = Field(description="documentation URL")
