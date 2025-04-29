# agents/developer.py
from typing import Dict, List
import json, textwrap

from llm_factory import get_llm
from langchain.prompts import ChatPromptTemplate
from tools.file_tools import write_file
from tools.common_tools import comment_tool

llm = get_llm(temperature=0.15)

project_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            textwrap.dedent("""\
            You are a senior full-stack developer. Based on the tasks below,
            produce the ENTIRE source tree for a small, static web site.
            Return ONLY valid JSON – an array of objects with keys:
              • "path": relative path+filename (e.g. "index.html", "css/style.css")
              • "content": full file contents as UTF-8 text
            Do NOT wrap the JSON in markdown fences.
            """)
        ),
        ("human", "{tasks_block}"),
    ]
)

def implement(state: Dict) -> Dict:
    tasks: List[str] | None = state.get("tasks")
    chat_id: str | None = state.get("chat_id")
    if not tasks or not chat_id:
        raise ValueError("Developer needs 'tasks' and 'chat_id' in state")

    tasks_block = "\n".join(tasks)
    response_text = (project_prompt | llm).invoke({"tasks_block": tasks_block}).content

    try:
        file_specs = json.loads(response_text)  # expect a list[dict]
    except Exception:
        # one safe fallback file if JSON was invalid
        file_specs = [{"path": "README.md", "content": comment_tool.func(tasks_block)}]

    created_paths: List[str] = []
    seen: set[str] = set()

    for spec in file_specs:
        path, content = spec.get("path"), spec.get("content", "")
        if not path or path in seen:
            # skip duplicates or malformed entries
            continue
        abs_path = write_file.invoke(
            {"chat_id": chat_id, "rel_path": path, "text": content}
        )
        created_paths.append(abs_path)
        seen.add(path)
        print(f"[Dev] wrote {abs_path}")

    return {"implementation_steps": created_paths}
