from pydantic import BaseModel


class QueueModel(BaseModel):
    user_id: int
    subjects: list
    rank: str

    class Config:
        orm_mode = True
