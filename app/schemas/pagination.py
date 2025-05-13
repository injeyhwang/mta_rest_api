from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

# a generic type parameter for Pagination results
T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    total: int = Field(description="Total number of items across all pages")
    offset: int = Field(description="Number of items skipped")
    limit: int = Field(description="Maximum number of items per page")
    results: List[T] = Field(description="The current page of items")


class ListResponse(BaseModel, Generic[T]):
    total: int = Field(description="Total number of items across all pages")
    results: List[T] = Field(description="The current page of items")
