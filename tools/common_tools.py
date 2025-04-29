# tools/common_tools.py
from langchain.agents import Tool

# ── Demo 1 — existing helper ────────────────────────────────────────────────
def uppercase(text: str) -> str:
    """Return the input string in UPPER-CASE."""
    return text.upper()


uppercase_tool = Tool(
    name="UppercaseTool",
    func=uppercase,
    description="Convert any text to UPPER-CASE."
)

# ── Demo 2 — NEW helper the Developer agent will use ───────────────────────
def comment_out(text: str) -> str:
    """
    Prefix every non-blank line with '# ' so it becomes a Python comment
    block. Handy for turning plain text into TODO comments.
    """
    return "\n".join(
        f"# {line}" if line.strip() else "" for line in text.splitlines()
    )


comment_tool = Tool(
    name="CommentOutTool",
    func=comment_out,
    description="Turn each line of text into a Python comment beginning with '# '."
)
