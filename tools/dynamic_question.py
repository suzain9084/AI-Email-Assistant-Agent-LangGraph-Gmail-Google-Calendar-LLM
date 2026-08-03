from typing import Literal

from langchain_core.tools import tool
from langgraph.types import interrupt

@tool
def dynamic_question(
    question: str,
    options: list[str] | None = None,
) -> str:
    """
    Ask the user a question and pause the graph until an answer is provided.

    Use this tool whenever required information is missing or ambiguous.
    """

    answer = interrupt(
        {
            "type": "question",
            "question": question,
            "options": options or [],
        }
    )

    return {
        "question": question,
        "answer": answer
    }