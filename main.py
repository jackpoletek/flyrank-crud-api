from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class TaskInput(BaseModel):
    title: str = ""
    done: bool = False

    
@app.exception_handler(HTTPException)
def handle_http_error(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


tasks = [
{"id": 1, "title": "Make coffee", "done": False},
{"id": 2, "title": "Walk the dog", "done": False},
{"id": 3, "title": "Finish assignment 1", "done": True},
]


def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


@app.get("/")
def describe_api():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health")
def check_health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


def next_task_id():
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


@app.post("/tasks", status_code=201, summary="Create a task")
def create_task(task_input: TaskInput):
    title = task_input.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    new_task = {"id": next_task_id(), "title": title, "done": False}
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, task_input: TaskInput):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    title = task_input.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    task["title"] = title
    task["done"] = task_input.done
    return task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    tasks.remove(task)
    return None
