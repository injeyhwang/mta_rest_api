from sqlmodel import Field, SQLModel


class Calendar(SQLModel, table=True):
    service_id: str = Field(primary_key=True, description="Unique identifier for the service")
    monday: bool = Field(description="Service operates on Mondays")
    tuesday: bool = Field(description="Service operates on Tuesdays")
    wednesday: bool = Field(description="Service operates on Wednesdays")
    thursday: bool = Field(description="Service operates on Thursdays")
    friday: bool = Field(description="Service operates on Fridays")
    saturday: bool = Field(description="Service operates on Saturdays")
    sunday: bool = Field(description="Service operates on Sundays")
    start_date: str = Field(description="Start date of service in YYYYMMDD format")
    end_date: str = Field(description="End date of service in YYYYMMDD format")
