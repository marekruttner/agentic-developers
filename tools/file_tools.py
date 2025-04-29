# tools/file_tools.py
from __future__ import annotations
from pathlib import Path
from typing import List
from uuid import uuid4
import os, json

# ---------------------------------------------------------------------------
# 1) get safe_join from LangChain *if* the current version exports it
# 2) otherwise fall back to a local, secure implementation
# ---------------------------------------------------------------------------
try:
    from langchain_community.tools.file_management.utils import safe_join  # present in LC ≥0.1.17
except (ImportError, AttributeError):                                      # older builds
    # Prevent path-traversal by ensuring the resolved path stays inside root
    def safe_join(root: Path | str, rel_path: str) -> str:
        root_path = Path(root).resolve()
        target = (root_path / rel_path).resolve()
        if not str(target).startswith(str(root_path)):
            raise ValueError("Unsafe path (possible traversal): " + rel_path)
        return str(target)

# ----------------------------- workspace helpers ---------------------------
def ensure_workspace(chat_id: str) -> Path:
    """
    Guarantee output/<chat_id>/ exists and return its Path object.
    os.makedirs(..., exist_ok=True) is the simplest cross-version way to create
    nested dirs safely :contentReference[oaicite:1]{index=1}
    """
    root = Path("output") / chat_id
    root.mkdir(parents=True, exist_ok=True)
    return root.resolve()

# ----------------------------- LangChain tools -----------------------------
from langchain_core.tools import tool  # LC 0.1+ decorator

@tool
def write_file(chat_id: str, rel_path: str, text: str) -> str:
    """
    Save UTF-8 text into <workspace>/<rel_path>, creating folders when needed.
    Returns the absolute file path.
    """
    root = ensure_workspace(chat_id)
    abs_path = Path(safe_join(root, rel_path))
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_text(text, encoding="utf-8")           # standard write :contentReference[oaicite:2]{index=2}
    return str(abs_path)

@tool
def read_file(chat_id: str, rel_path: str) -> str:
    """
    Read UTF-8 text from <workspace>/<rel_path>.
    """
    root = ensure_workspace(chat_id)
    abs_path = Path(safe_join(root, rel_path))
    return abs_path.read_text(encoding="utf-8")
