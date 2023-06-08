from typing import Optional

from pydantic import BaseModel


class GameModel(BaseModel):
    user_id: int
    opponent_id: int
    task: str
    winner: Optional[int]

    class Config:
        orm_mode = True
