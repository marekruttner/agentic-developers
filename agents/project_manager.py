from typing import Dict, List
from uuid import uuid4

from llm_factory import get_llm
from langchain.prompts import ChatPromptTemplate

llm = get_llm(temperature=0)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a meticulous project-planning assistant. "
            "Break the description into 3-7 concise tasks, each on its own line."
        ),
        ("human", "{description}"),
    ]
)

def plan_tasks(state: Dict) -> Dict:
    # Create chat_id once
    chat_id = state.get("chat_id") or str(uuid4())
    print("[PM] chat_id:", chat_id)

    """Return a new key 'tasks' instead of mutating the incoming dict."""
    description: str = state.get("description", "create basic web page")
    if not description:
        raise ValueError("State must contain a non-empty 'description' field")

    resp = (prompt | llm).invoke({"description": description})
    tasks: List[str] = [ln.strip() for ln in resp.content.splitlines() if ln.strip()]

    print("[PM] Planned tasks:", tasks)
    return {"tasks": tasks, "chat_id": chat_id}  # <-- important
