import os
from dotenv import load_dotenv

from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from state import EmailAgentState
from tools.gmail_tools import EMAIL_TOOLS
from tools.calendar_tools import CALENDAR_TOOLS
from tools.dynamic_question import dynamic_question
from langgraph.types import Command
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
)

class ReplyStructure(BaseModel):
    to: str = Field(description="Recipient email")
    subject: str = Field(description="Email subject")
    message: str = Field(description="Email body")
    cc: list[str] = Field(default_factory=list)
    bcc: list[str] = Field(default_factory=list)

tools = [
    *EMAIL_TOOLS,
    *CALENDAR_TOOLS,
    DuckDuckGoSearchRun(),
]

context_agent = create_react_agent(
    model=llm,
    tools=tools,
)

structured_llm = llm.with_structured_output(ReplyStructure)
reply_agent = create_react_agent(
    model=llm,
    tools=[dynamic_question, *EMAIL_TOOLS, *CALENDAR_TOOLS]
)

context_prompt = ChatPromptTemplate.from_template(
    """
        You are an email assistant.

        Your task is to gather enough information to reply to the email.

        Available tools:

        - Gmail Search
        - Gmail Read
        - Google Calendar
        - Web Search

        Instructions:

        1. Search previous related emails.
        2. Search for earlier conversations with the sender.
        3. Check upcoming calendar events if scheduling is mentioned.
        4. Perform a web search only if external information is needed.

        Return ONLY a concise summary of everything useful for generating a reply.

        Email:

        {email}
    """
)

reply_prompt = ChatPromptTemplate.from_template(
    """
        You are an AI executive email assistant.

        Generate a professional reply.

        Original Email:

        {email}

        Context:

        {context}

        Information from user:

        {information}

        Instructions:

        - Reply naturally.
        - If a meeting is required, mention available meeting details.
        - If a calendar event already exists, reference it.
        - If no context is useful, simply answer the email.

        Return the response in the required structured format.
"""
)

def generate_context_node(state: EmailAgentState):
    chain = context_prompt | context_agent
    result = chain.invoke(
        {
            "email": state["message"]
        }
    )
    context = result["messages"][-1].content
    return {
        "context": context
    }


def generate_reply_node(state: EmailAgentState):
    chain = reply_prompt | reply_agent
    agent_result = chain.invoke(
        {
            "email": state["message"],
            "context": state["context"],
            "information": state["question_answer"]
        }
    )
    ai_message = next(
        msg
        for msg in reversed(agent_result["messages"])
        if isinstance(msg, AIMessage)
    )

    if isinstance(ai_message.content, list):
        final_text = "".join(
            block["text"]
            for block in ai_message.content
            if block.get("type") == "text"
        )
    else:
        final_text = ai_message.content

    reply = structured_llm.invoke(
    f"""
        Convert the following email into ReplyStructure.

        Email:

        {final_text}
    """
    )
    return {"reply": reply}

builder = StateGraph(EmailAgentState)
builder.add_node("generate_context", generate_context_node)
builder.add_node("generate_reply", generate_reply_node)

builder.add_edge(START, "generate_context",)
builder.add_edge("generate_context", "generate_reply",)
builder.add_edge("generate_reply", END)

memory = InMemorySaver()
agent = builder.compile()

if __name__ == "__main__":

    state = {
        "message": """
Subject: Client Meeting

Hi,

Please schedule a meeting with the client sometime next week and send them the invitation.

Thanks,
Sarah
"""
    }
    config = {
        "configurable": {
            "thread_id": "email-thread-1"
        }
    }

    result = agent.invoke(state, config=config)
    while "__interrupt__" in result:
        interrupt = result["__interrupt__"][0].value

        print("\n" + "=" * 60)
        print("Assistant needs more information")
        print("=" * 60)

        print(interrupt["question"])

        if interrupt.get("options"):
            print("\nOptions:")
            for i, option in enumerate(interrupt["options"], start=1):
                print(f"{i}. {option}")

        answer = input("\nYour answer: ")

        result = agent.invoke(
            Command(
                resume=answer,
                update={
                    "question_answer": [{
                        "question": AIMessage(interrupt["question"]),
                        "answer": HumanMessage(answer)
                    }]
                }
            ),
            config=config,
        )

    print("\n" + "=" * 60)
    print("Generated Reply")
    print("=" * 60)

    print(result["reply"].model_dump_json(indent=2))
