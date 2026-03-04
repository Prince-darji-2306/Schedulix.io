from core.llm_engine import get_llm
from langgraph.graph import StateGraph, END
from schemas.plan import PlanState

def generate_plans_node(state: PlanState):
    llm = get_llm(is_temp = True)
    prompt = (
        f"Generate 3 diverse and distinct plans for the following task:\n"
        f"Title: {state['title']}\n"
        f"Description: {state['description']}\n"
        f"Current Time: {state['current_time']}\n"
        f"Deadline: {state['deadline']}\n"
        f"Make sure they are truly different (e.g., one fast, one thorough, one creative).\n"
        f"They are should be listed in less than or equal to 12 points not more than that."
    )
    response = llm.invoke(prompt)
    return {"plans": [response.content]}

def finalize_plan_node(state: PlanState):
    llm = get_llm()
    prompt = (
        f"Based on these 3 diverse ideas:\n{state['plans'][0]}\n"
        f"Create a single, optimized, and comprehensive finalized plan for the task: {state['title']}.\n"
        f"The current time is {state['current_time']} and the deadline is {state['deadline']}.\n"
        f"Generate a list of adaptive subtasks (minimum 3, maximum 10) based on the task's complexity.\n"
        f"Each subtask must have a 'subtask' (title), 'description' (detailed steps), and 'time_to' (scheduled time in HH:MM format).\n"
        f"CRITICAL: Schedule 'time_to' for each subtask in incremental order start after {state['current_time']} and must finish by {state['deadline']}.\n"
        f"Return ONLY a JSON object with two keys:\n"
        f"1. 'markdown_plan': A beautiful markdown summary of the whole plan.\n"
        f"2. 'subtasks': A JSON array of the subtask objects.\n"
    )
    response = llm.invoke(prompt)
    content = response.content.strip()
    # Handle potential code blocks
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
    
    return {"final_plan": content}

# Create Graph
workflow = StateGraph(PlanState)
workflow.add_node("generator", generate_plans_node)
workflow.add_node("finalizer", finalize_plan_node)
workflow.set_entry_point("generator")
workflow.add_edge("generator", "finalizer")
workflow.add_edge("finalizer", END)
ai_graph = workflow.compile()
