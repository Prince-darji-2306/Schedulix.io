from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    deadline_date: str
    time: str
    status: Optional[str] = "Pending"
