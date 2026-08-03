import os

from langgraph.types import interrupt
from langgraph.graph import StateGraph, START, END

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from state import EmailAgentState
from nodes.generate_reply import ReplyStructure
from nodes.send_email_node import email_send_node
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
)

structured_llm = llm.with_structured_output(ReplyStructure)

prompt = ChatPromptTemplate.from_template(
    """
You are an executive email assistant.

Regenerate the following email according to the user's feedback.

Original Email

{email}

Context

{context}

User Feedback

{instruction}

Return ONLY the regenerated email in ReplyStructure format.
"""
)

def user_approval(state: EmailAgentState):

    reply = state["reply"]

    print("\n" + "=" * 60)
    print("Generated Email")
    print("=" * 60)
    print(f"To      : {reply.to}")
    print(f"Subject : {reply.subject}")
    print()
    print(reply.message)
    print("=" * 60)

    answer = interrupt(
        {
            "question": "Do you want to send this email?",
            "options": [
                "Yes",
                "No"
            ]
        }
    )

    approved = str(answer).strip().lower() in {
        "1",
        "yes",
        "y",
        "true",
    }

    return {
        "user_approval": approved
    }


def approval_router(state: EmailAgentState):
    if state["user_approval"]:
        return "approve"
    return "regenerate"


def re_generate_instruction(state: EmailAgentState):
    answer = interrupt({
        "question": "How would you like to modify the email?"
    })
    return {
        "refine_suggestion": answer
    }


def re_generate_mail(state: EmailAgentState):
    chain = prompt | structured_llm
    reply = chain.invoke({
        "email": f"""
            To: {state["reply"].to}

            Subject:
            {state["reply"].subject}

            Body:
            {state["reply"].message}
        """,
        "instruction": state["refine_suggestion"],
        "context": state["context"],
    })

    return {
        "reply": reply
    }

builder = StateGraph(EmailAgentState)

builder.add_node("user_approval", user_approval)
builder.add_node("re_generate_instruction", re_generate_instruction)
builder.add_node("re_generate_mail", re_generate_mail)
builder.add_node("final_operation", email_send_node)


builder.add_edge(START, "user_approval")

builder.add_conditional_edges(
    "user_approval",
    approval_router,
    {
        "approve": "final_operation",
        "regenerate": "re_generate_instruction",
    },
)

builder.add_edge(
    "re_generate_instruction",
    "re_generate_mail",
)

builder.add_edge(
    "re_generate_mail",
    "user_approval",
)

builder.add_edge(
    "final_operation",
    END,
)

approval_graph = builder.compile()