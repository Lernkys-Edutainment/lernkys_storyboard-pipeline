"""
storyboard_schema.py

Pydantic models for storyboard generation.
"""

from typing import List
from pydantic import BaseModel


class StoryboardBeat(BaseModel):
    beat_id: str
    source_text: str
    visual: str
    ost: str
    dialogue: str


class Storyboard(BaseModel):
    beats: List[StoryboardBeat]