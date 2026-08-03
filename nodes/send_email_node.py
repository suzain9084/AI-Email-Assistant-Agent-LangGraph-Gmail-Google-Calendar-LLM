from state import EmailAgentState
from tools.gmail_tools import send_gmail_message
from langchain_core.messages import AIMessage


def email_send_node(state: EmailAgentState):
    reply = state["reply"]

    email = f"""
        To: {reply.to}
        Subject: {reply.subject}
        CC: {", ".join(reply.cc)}
        BCC: {", ".join(reply.bcc)}

        {reply.message}
    """

    try:
        result = send_gmail_message.invoke(
            {
                "message": email,
            }
        )

        return {"gmail_response": result}

    except Exception as e:
        return {"gmail_response": str(e)}