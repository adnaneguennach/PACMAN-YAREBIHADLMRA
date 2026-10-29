from pydantic import BaseModel, Field
from typing import List


class LevelConfig(BaseModel):
    """Configuration for a single game level."""

    width: int = Field(ge=5)
    height: int = Field(default=15, ge=5)


class Config(BaseModel):
    """Store and validate the Pacman game configuration."""

    highscore_filename: str
    lives: int = Field(ge=1)
    pacgum: int = Field(ge=0)
    points_per_pacgum: int = Field(ge=0)
    points_per_super_pacgum: int = Field(ge=0)
    points_per_ghost: int = Field(ge=0)
    level_max_time: int = Field(ge=1)
    seed: int = Field(ge=0)
