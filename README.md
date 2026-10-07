# Lead Automation API

A lightweight FastAPI service designed for lead capture and automation workflows.

## Why this project?
This project demonstrates REST API design, webhook-style data intake, validation, SQLite persistence, and automation-friendly JSON responses. It can be connected directly to n8n, Make, Zapier, CRMs, Slack, email tools, or custom SaaS workflows.

## Features
- `POST /webhook/lead` lead capture endpoint
- Email validation with Pydantic
- Duplicate protection
- SQLite persistence
- Automation-ready event payload
- `GET /leads` listing endpoint
- Health endpoint
- Basic test coverage

## Tech Stack
Python, FastAPI, SQLite, REST API, Webhooks, Pytest

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open Swagger docs at `http://127.0.0.1:8000/docs`.

## Example request
```json
{
  "name": "Atilla Balkir",
  "email": "atilla@example.com",
  "company": "Demo Company",
  "source": "landing-page"
}
```

## n8n Integration Idea
Use an n8n Webhook or HTTP Request node to send incoming form leads to `/webhook/lead`, then route the returned payload to Gmail, Slack, Google Sheets, HubSpot or another CRM.
