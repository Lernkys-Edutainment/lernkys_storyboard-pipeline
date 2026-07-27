"""
storyboard_schema.py

Pydantic models for storyboard generation.
"""

from typing import List

from pydantic import BaseModel, Field


class StoryboardBeat(BaseModel):
    beat_id: str = Field(
        ...,
        min_length=1,
        description="Unique beat identifier"
    )

    source_text: str = Field(
        ...,
        min_length=1,
        description="Original narration for the beat"
    )

    visual: str = Field(
        ...,
        min_length=1,
        description="Storyboard visual description"
    )

    ost: str = Field(
        ...,
        min_length=1,
        description="On-screen text"
    )

    dialogue: str = Field(
        ...,
        min_length=1,
        description="Dialogue or narration"
    )

    graphics_type: str = Field(
        default="Other",
        description="Graphics or animation style of the beat"
    )


class Storyboard(BaseModel):
    beats: List[StoryboardBeat] = Field(
        ...,
        min_length=1,
        description="List of storyboard beats"
    )