from pydantic import BaseModel


class QueueModel(BaseModel):
    user_id: int
    subject: str
    rank: str

    class Config:
        orm_mode = True
