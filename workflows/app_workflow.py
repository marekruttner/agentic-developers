from langgraph.graph import StateGraph
from typing import List
from typing_extensions import TypedDict

from agents.project_manager import plan_tasks
from agents.developer import implement

class AppState(TypedDict, total=False):
    description: str
    tasks: List[str]
    implementation_steps: List[str]

def build_workflow():
    sg = StateGraph(AppState)
    sg.add_node("ProjectManager", plan_tasks)
    sg.add_node("Developer", implement)

    sg.set_entry_point("ProjectManager")
    sg.add_edge("ProjectManager", "Developer")

    return sg.compile()
