from typing import List, TypedDict

class PlanState(TypedDict):
    title: str
    description: str
    current_time: str
    deadline: str
    plans: List[str]
    final_plan: str
