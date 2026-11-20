from pydantic import BaseModel, Field


class ThumbnailReview(BaseModel):
    rating: int = Field(
        ...,
        ge=1,
        le=10,
        description="Thumbnail quality rating from 1 to 10"
    )
    critique: str = Field(
        ...,
        min_length=10,
        description="Actionable suggestions for improving the thumbnail"
    )