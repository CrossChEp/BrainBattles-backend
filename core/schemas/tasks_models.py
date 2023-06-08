from typing import Optional

from pydantic import BaseModel


class TaskAddModel(BaseModel):
    """Scheme of task
        fields:
        name: str
            task name
        subject: str
            task's subject
        content: str
            task's content
        right_answer: str
            task's right answer
        scores: float
            max scores for this task
        rank: str
            rank of task
    """
    name: str
    subject: str
    content: str
    right_answer: str
    scores: float
    rank: str

    class Config:
        orm_mode = True


class TaskUpdateModel(BaseModel):
    name: Optional[str]
    subject: Optional[str]
    content: Optional[str]
    right_answer: Optional[str]
    scores: Optional[int]
    rank: Optional[str]

    class Config:
        orm_mode = True


class TaskGetModel(BaseModel):
    id: int
    name: str
    subject: str
    content: str
    rank: str
    state: str

    class Config:
        orm_mode = True
