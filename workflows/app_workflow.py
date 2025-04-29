# workflows/app_workflow.py
from langgraph.graph import StateGraph
from typing_extensions import TypedDict, List

from agents.project_manager import plan_tasks          # <-- use the function directly
from agents.developer     import implement

class AppState(TypedDict, total=False):
    description: str
    chat_id: str
    tasks: List[str]
    implementation_steps: List[str]

def build_workflow():
    sg = StateGraph(AppState)

    sg.add_node("ProjectManager", plan_tasks)          # <-- was create_agent()
    sg.add_node("Developer", implement)

    sg.set_entry_point("ProjectManager")
    sg.add_edge("ProjectManager", "Developer")

    return sg.compile()
