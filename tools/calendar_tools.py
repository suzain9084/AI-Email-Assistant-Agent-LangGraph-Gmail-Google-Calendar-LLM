from googleapiclient.discovery import build
from langchain_google_community import CalendarToolkit
from auth.google_auth import get_google_credentials

creds = get_google_credentials()

calendar_service = build(
    "calendar",
    "v3",
    credentials=creds,
)

toolkit = CalendarToolkit(
    api_resource=calendar_service
)

calendar_tools = {
    tool.name: tool
    for tool in toolkit.get_tools()
}

create_calendar_event = calendar_tools["create_calendar_event"]
update_calendar_event = calendar_tools["update_calendar_event"]
delete_calendar_event = calendar_tools["delete_calendar_event"]
move_calendar_event = calendar_tools["move_calendar_event"]
get_current_datetime = calendar_tools["get_current_datetime"]
get_calendars_info = calendar_tools["get_calendars_info"]

CALENDAR_TOOLS = [
    get_current_datetime,
    get_calendars_info,
    create_calendar_event,
    update_calendar_event,
    move_calendar_event,
    delete_calendar_event,
]