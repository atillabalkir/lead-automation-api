from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone
import sqlite3

DB = 'leads.db'
app = FastAPI(title='Lead Automation API', version='1.0.0')

class LeadIn(BaseModel):
    name: str
    email: EmailStr
    company: str | None = None
    source: str = 'website'


def init_db():
    with sqlite3.connect(DB) as con:
        con.execute('''CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            company TEXT,
            source TEXT,
            created_at TEXT NOT NULL
        )''')

@app.on_event('startup')
def startup():
    init_db()

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/webhook/lead')
def create_lead(lead: LeadIn):
    created_at = datetime.now(timezone.utc).isoformat()
    try:
        with sqlite3.connect(DB) as con:
            cur = con.execute(
                'INSERT INTO leads(name,email,company,source,created_at) VALUES (?,?,?,?,?)',
                (lead.name, lead.email, lead.company, lead.source, created_at)
            )
            lead_id = cur.lastrowid
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail='Lead already exists')

    return {
        'id': lead_id,
        'message': 'Lead captured successfully',
        'automation_payload': {
            'event': 'lead.created',
            'lead': lead.model_dump(),
            'created_at': created_at
        }
    }

@app.get('/leads')
def list_leads():
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute('SELECT * FROM leads ORDER BY id DESC').fetchall()
    return [dict(r) for r in rows]
