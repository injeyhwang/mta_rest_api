from sqlmodel import Field, SQLModel


class CalendarDate(SQLModel, table=True):
    service_id: str = Field(
        primary_key=True,
        foreign_key="calendar.service_id",
        description="Service ID that this exception applies to")
    date: str = Field(
        primary_key=True,
        description="Date in YYYYMMDD format when service exception occurs")
    exception_type: int = Field(
        description="Type of exception (1=service added, 2=service removed)")
