# Task API

A small CRUD API for managing a to-do list. Built with FastAPI. Data lives in memory only —
it resets every time the server restarts (there's no database yet, that's next week).

## How to run it

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The server runs at `http://localhost:8000`. Interactive docs (Swagger UI) are at
`http://localhost:8000/docs`.

## Endpoints

| Method | Path           | What it does                                 |
|--------|----------------|--------------------------------------------  |
| GET    | `/`            | API info                                     |
| GET    | `/health`      | Health check — `{"status": "ok"}`            |
| GET    | `/tasks`       | List all tasks                               |
| GET    | `/tasks/{id}`  | Get one task (404 if it doesn't exist)       |
| POST   | `/tasks`       | Create a task (400 if title is missing)      |
| PUT    | `/tasks/{id}`  | Replace a task's title/done (404 if unknown) |
| DELETE | `/tasks/{id}`  | Delete a task (404 if unknown)               |

## Example

```
$ curl -i http://localhost:8000/tasks/1
HTTP/1.1 200 OK
content-type: application/json

{"id":1,"title":"Buy milk","done":false}
```

## Swagger screenshot

https://github.com/jackpoletek/flyrank-crud-api/blob/main/docs-screenshot.png

## Notes

- No database yet — tasks live in a plain Python list, so a server restart wipes them.
- All error responses use the shape `{"error": "message"}`.
