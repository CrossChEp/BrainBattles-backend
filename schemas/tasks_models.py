from pydantic import BaseModel


class TaskModel(BaseModel):
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

