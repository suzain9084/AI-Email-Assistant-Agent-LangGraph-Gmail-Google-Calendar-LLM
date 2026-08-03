# AI Email Assistant Agent

An intelligent email assistant built using **LangGraph**, **LangChain**, and **Groq LLM** that automates email understanding, gathers context from multiple sources, generates smart replies, and supports Human-in-the-Loop approval before sending emails.

---

## Overview

This project demonstrates how Agentic AI can automate professional email workflows by combining multiple tools inside a graph-based architecture.

Instead of using a single LLM prompt, the agent coordinates several independent components to analyze emails, retrieve additional context, generate responses, and request user approval before sending.

---

## Features

- Read incoming emails using Gmail API
- Generate context-aware email replies
- Google Calendar integration
- Web search integration
- Human-in-the-Loop approval
- Stateful workflow using LangGraph
- Structured outputs using Pydantic
- Modular node-based architecture
- Tool calling with LangChain

---

## Architecture

```
Incoming Email
        │
        ▼
 Read Gmail Context
        │
        ▼
 Search Calendar
        │
        ▼
 Search Web (Optional)
        │
        ▼
 Ask Dynamic question
     to user
        │
        ▼
 Generate Reply
        │
        ▼
     User Approval? <───────────────────────|          
      /         \                           |
    Yes         No                          |
     │           │                          |
Send Email      Take Instruction            |
add Event to    from user to refine         |
calendar                │                   |
                        ▼                   |
                re generte response
                        |
                        ────────────────────|
```

---

## Tech Stack

- Python
- LangGraph
- LangChain
- Groq LLM
- Gmail API
- Google Calendar API
- DuckDuckGo Search
- Pydantic

---

## Project Structure

```
email_agent/

├── nodes/
├── tools/
├── workflow/
├── state.py
├── app.py
├── requirements.txt
└── README.md
```

---

## Workflow

1. Monitor incoming emails.
2. Retrieve email content.
3. Collect relevant context using Gmail and Google Calendar.
4. Perform web search when additional information is required.
5. Generate an AI-powered response.
6. Ask Dynamic Question required to user to generate respose
7. Ask the user for approval.
8. Send the email after confirmation.

---

## Learning Outcomes

This project helped me understand:

- Agentic AI
- LangGraph workflows
- State management
- Tool calling
- Human-in-the-Loop systems
- Google API integration
- LLM orchestration
- Modular software architecture

---

## Future Improvements

- Memory for previous conversations
- Vector database integration
- RAG over historical emails
- Multi-agent architecture
- Streaming responses
- Persistent state (SQLite/PostgreSQL)
- Gmail Push Notifications
- Docker deployment
- Authentication dashboard
- Unit and integration testing

---

## Installation

```bash
git clone https://github.com/your-username/email-agent.git

cd email-agent

pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key

GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

Run the application:

```bash
python app.py
```

---

## Disclaimer

This project is intended for educational purposes and demonstrates how modern AI agents can orchestrate multiple tools to automate email workflows.

---

## Author

**Suzain**

Final Year B.Tech Student

Passionate about AI Agents, LLMs, System Design, and Backend Engineering.