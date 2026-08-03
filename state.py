from typing import TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage
import operator

class EmailReply(TypedDict):
    to: str
    subject: str
    message: str
    cc: list[str]
    bcc: list[str]


# later convert it into AImessage and human messages
class Question(TypedDict):
    question: AIMessage
    answer: HumanMessage

class EmailAgentState(TypedDict):
    thread_id: str
    e_from: str
    message: str
    subject: str
    summary: str
    context: str
    reply: EmailReply
    user_approval: bool = False
    refine_suggestion: str
    question_answer:  Annotated[list[Question], operator.add]
    gmail_response: str

    


