from typing import Dict, List
from llm_factory import get_llm
from langchain.prompts import ChatPromptTemplate
from tools.common_tools import comment_tool

llm = get_llm(temperature=0.2)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a senior developer. For each task, output one-sentence "
            "implementation guidance."
        ),
        ("human", "{tasks}"),
    ]
)

def implement(state: Dict) -> Dict:
    tasks: List[str] | None = state.get("tasks")
    if not tasks:
        raise ValueError("Developer needs a non-empty 'tasks' list in state")

    resp = (prompt | llm).invoke({"tasks": "\n".join(tasks)})
    outlines = [ln.strip() for ln in resp.content.splitlines() if ln.strip()]
    commented = [comment_tool.func(t) for t in outlines]

    print("[Dev] Implementation steps:")
    for c in commented:
        print(c)

    return {"implementation_steps": commented}   # <-- important
