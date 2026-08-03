import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from state import EmailAgentState

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)

class OutputStructure(BaseModel):
    summary: str = Field(
        description="A concise summary of the email containing all important information."
    )

model = llm.with_structured_output(OutputStructure)

prompt = ChatPromptTemplate.from_template(
    """
You are an email summarization assistant.

Your task is to summarize the following email while preserving all important
information.

Instructions:
- Keep the summary concise.
- Include important dates, deadlines, names, and action items.
- Do not add information that is not present in the email.

Email:
{email}
"""
)

chain = prompt | model

async def summary_node(state: EmailAgentState) -> EmailAgentState:
    email = (
        f"Subject:\n{state['subject']}\n\n"
        f"Message:\n{state['message']}"
    )

    result = await chain.invoke(
        {
            "email": email
        }
    )

    return {
        "summary": result.summary
    }