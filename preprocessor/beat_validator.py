from typing import List
from pydantic import BaseModel, Field


class Beat(BaseModel):
    beat_id: int
    text: str = Field(min_length=1)


class BeatList(BaseModel):
    beats: List[Beat]


def validate_beats(data):
    return BeatList.model_validate(data)