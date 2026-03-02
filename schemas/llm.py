from pydantic import BaseModel
from typing import Optional

class GetTemp(BaseModel):
    is_temp: Optional[bool] = False
