# Recruitment Pipeline - Software Engineer Intern Task

## Overview
This repository contains a full-stack implementation of a recruitment pipeline management tool. The project encompasses both the frontend and backend requirements, providing a functional Kanban board for candidate tracking seamlessly integrated with a RESTful API.

## Tech Stack
- Backend: FastAPI, SQLAlchemy, SQLite
- Frontend: React (Vite), CSS Modules, @hello-pangea/dnd

## Project Structure
```text
.
├── recruitment-pipeline-api/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routers/
│   │   ├── schemas.py
│   │   ├── seed.py
│   │   └── services/
│   └── requirements.txt
└── recruitment-pipeline-ui/
    ├── package.json
    └── src/
        ├── App.jsx
        ├── api/
        └── components/
```

## Setup & Run

### Backend
1. Navigate to the backend directory:
   ```bash
   cd recruitment-pipeline-api
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Confirm the server is running on `http://localhost:8000`. The interactive Swagger API documentation is available at `http://localhost:8000/docs`.

### Frontend
1. Open a new terminal window and navigate to the frontend directory:
   ```bash
   cd recruitment-pipeline-ui
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Confirm the application is running on `http://localhost:5173`. Note: The frontend requires the backend server to be running on port 8000 for data fetching to work correctly.

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | `/candidates` | Retrieves a list of candidates. Supports `stage` filter, `skip`, `limit`, `sort_by`, and `order` query params. |
| POST | `/candidates` | Creates a new candidate record. |
| GET | `/candidates/{id}` | Retrieves a specific candidate by ID. |
| PUT | `/candidates/{id}` | Updates an existing candidate's full details. |
| PATCH | `/candidates/{id}/stage` | Updates only the stage of a specific candidate. |
| DELETE | `/candidates/{id}` | Deletes a candidate record by ID. |

## Assumptions & Decisions
- SQLite was chosen over Postgres/Mongo for zero-setup local execution and grading. The use of SQLAlchemy makes swapping out the underlying database a low-effort task.
- CSS Modules were chosen to keep styles strictly scoped to components without introducing a runtime dependency (Tailwind was excluded per the brief's constraints).
- Stage names are treated as a fixed set of four strings rather than a dynamic database structure, as the brief explicitly specifies exactly these four stages.
- The frontend drag-and-drop interaction calls the real PATCH endpoint with an optimistic UI update, rolling back the visual state immediately if the request fails.
- The backend seed script only populates the database if it is completely empty, ensuring that restarting the server does not result in duplicated data.

## Known Limitations / What I'd Add With More Time
- Authentication and authorization are not implemented (out of scope per the brief).
- Automated tests are currently absent.
- The frontend does not expose a UI for pagination or sorting, though the backend fully supports both via query parameters.

## Demo
[Placeholder line: link to screen recording or deployed URL, to be added]
