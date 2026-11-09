from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

# "מסד נתונים" בזיכרון
tasks = []
counter = 1

@app.get("/tasks")
def get_tasks(priority: Optional[str] = None):
    if priority is not None:
        try:
            p_val = int(priority)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid priority filter: must be an integer between 1 and 3"
            )
        if p_val < 1 or p_val > 3:
            raise HTTPException(
                status_code=400,
                detail="Invalid priority filter: must be an integer between 1 and 3"
            )
        return [task for task in tasks if task["priority"] == p_val]
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def add_task(task: dict):
    global counter
    priority = task.get("priority", 2)

    # בפייתון bool יורש מ-int, לכן בודקים גם שאינו bool
    if type(priority) is not int or priority < 1 or priority > 3:
        raise HTTPException(
            status_code=400,
            detail="Invalid priority: must be an integer between 1 (high) and 3 (low)"
        )

    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner"),
        "priority": priority
    }
    tasks.append(new_task)
    counter += 1
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")