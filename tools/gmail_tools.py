from langchain_google_community import GmailToolkit
from auth.google_auth import get_google_credentials
from googleapiclient.discovery import build

creds = get_google_credentials()

gmail_service = build(
    "gmail",
    "v1",
    credentials=creds,
)

gmail_toolkit = GmailToolkit(api_resource=gmail_service)

gmail_tools = {
    tool.name: tool
    for tool in gmail_toolkit.get_tools()
}

create_gmail_draft = gmail_tools["create_gmail_draft"]
send_gmail_message = gmail_tools["send_gmail_message"]
search_gmail = gmail_tools["search_gmail"]
get_gmail_message = gmail_tools['get_gmail_message']
get_gmail_thread = gmail_tools['get_gmail_thread']


EMAIL_TOOLS = [
    create_gmail_draft,
    send_gmail_message,
    search_gmail,
    get_gmail_message,
    get_gmail_thread
]
