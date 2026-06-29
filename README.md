# AI-AGent-Control-Pane

FastAPI boilerplate for building Python APIs.

## Project structure

```
.
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- api/
|   |   |-- __init__.py
|   |   |-- deps.py
|   |   `-- v1/
|   |       |-- __init__.py
|   |       `-- routes/
|   |           |-- __init__.py
|   |           |-- health.py
|   |           `-- agents.py
|   |-- core/
|   |   |-- __init__.py
|   |   `-- config.py
|   |-- models/
|   |   `-- __init__.py
|   |-- schemas/
|   |   |-- __init__.py
|   |   `-- agent.py
|   `-- services/
|       `-- __init__.py
|-- tests/
|   |-- test_agents.py
|   `-- test_health.py
|-- .env.example
|-- .gitignore
|-- requirements.txt
`-- requirements-dev.txt
```

## 1) Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2) Install dependencies

```powershell
pip install -r requirements-dev.txt
```

## 3) Configure environment variables

Copy `.env.example` to `.env` and update values as needed.

This project now uses PostgreSQL. For a DigitalOcean Managed Database, set `DATABASE_URL` in `.env` using the connection string format below:

```env
DATABASE_URL=postgresql+psycopg://doadmin:<password>@<host>:25060/defaultdb?sslmode=require
AGENTS_TABLE_NAME=agents
```

Use the host, password, and database name from your DigitalOcean database connection details.

## 4) Run the API

```powershell
uvicorn app.main:app --reload
```

Open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Sample endpoint

Create an agent:

```http
POST /v1/agents/
Content-Type: application/json

{
	"name": "billing-reconciler",
	"tenant_id": "tenant-123",
	"runtime": "python",
	"config": {
		"model": "gpt-4o-mini"
	}
}
```

## 5) Run tests

```powershell
pytest
```

Run only agent tests:

```powershell
pytest tests/test_agents.py
```