from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    FastAPI server configurations via pydantic-settings. All server configs and metadata info are
    defined here and utilized on server instantiation.
    """

    # App info
    app_name: str = "mta_rest_api"
    app_version: str = "0.1.4"
    app_description: str = "A simple REST API reverse proxy for MTA's complicated GTFS and GTFS-RT APIs."

    # API route prefix
    api_prefix: str = "/api"

    # CORS configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Debug mode
    debug: bool = True


settings = Settings()
