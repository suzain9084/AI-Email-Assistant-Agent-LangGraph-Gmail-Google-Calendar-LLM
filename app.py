from tools.gmail_tools import search_gmail
import time
from workflow.whole_workflow import start_agent
import uuid

print("Starting Gmail event monitor...")
last_checked_timestamp = int(time.time())

while True:
    try:
        current_run_time = int(time.time())

        query_string = f"after:{last_checked_timestamp}"
        print(f"Checking for emails since last timestamp using query: '{query_string}'")
        
        emails_found = search_gmail.invoke({"query": query_string})

        if emails_found:
            print("New email detected via timestamp trigger! Routing to Agent...")
            # print(emails_found)
            for email in emails_found:
                start_agent(email=email)
        
        last_checked_timestamp = current_run_time
            
    except Exception as e:
        print(f"Error checking emails: {e}")
    time.sleep(60)


