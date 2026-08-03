from nodes.summary import summary_node
from nodes.generate_reply import agent as reply_graph
from nodes.user_approval import approval_graph
from langgraph.graph import StateGraph, START, END
from state import EmailAgentState
from langgraph.checkpoint.memory import InMemorySaver

from uuid import uuid4
from langgraph.types import Command
from langchain_core.messages import AIMessage, HumanMessage

graph = StateGraph(EmailAgentState)

graph.add_node("summary_node", summary_node)
graph.add_node("reply_graph", reply_graph)
graph.add_node("approval_graph", approval_graph)

graph.add_edge(START, "summary_node")
graph.add_edge("summary_node", "reply_graph")
graph.add_edge("reply_graph", "approval_graph")
graph.add_edge("approval_graph", END)

memory = InMemorySaver()

email_agent = graph.compile(
    checkpointer=memory
)

def start_agent(email: str, thread_id: str | None = None):

    thread_id = thread_id or str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    state = {
        "message": email
    }

    result = email_agent.invoke(
        state,
        config=config,
    )

    while "__interrupt__" in result:
        data = result["__interrupt__"][0].value

        print(data["question"])

        if data.get("options"):
            for option in data["options"]:
                print("-", option)

        answer = input("> ")

        result = email_agent.invoke(
            Command(
                resume=answer,
                update={
                    "question_answer": [{
                        "question": AIMessage(content=data["question"]),
                        "answer": HumanMessage(content=answer)
                    }]
                }
            ),
            config=config,
        )

    return result