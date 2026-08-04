from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate

from state import EmailAgentState
from tools.calendar_tools import CALENDAR_TOOLS
from tools.gmail_tools import EMAIL_TOOLS
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    prompt="You are an email assistant. If the email requires any calendar action, perform it before sending the email."
)

tools = [
    *CALENDAR_TOOLS,
    *EMAIL_TOOLS,
]

agent = create_react_agent(
    model=llm,
    tools=tools
)

prompt = ChatPromptTemplate.from_messages(
    [
        HumanMessage(content="""
            To: {to}
            Subject: {subject}
            CC: {cc}
            BCC: {bcc}

            Body:
            {message}
        """)
    ]
)

def email_send_node(state: EmailAgentState):
    reply = state["reply"]
    chain = prompt | agent 

    try:
        result = chain.invoke({
            "to": reply["to"],
            "subject": reply["subject"],
            "cc": reply["cc"],
            "bcc": reply["bcc"],
            "message": reply["message"],
        })

        final_response = result["messages"][-1].content

        return {
            "gmail_response": final_response
        }

    except Exception as e:
        return {
            "gmail_response": str(e)
        }