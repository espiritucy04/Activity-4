import os
from fastapi import FastAPI, HTTPException, APIRouter, Depends, Request
from typing import Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Retrieve API Key securely from environment variables
API_KEY = os.getenv("LAB4_API_KEY")

# Middleware to verify API Key for authentication
def verify_api_key(request: Request):
    key_from_request = request.headers.get("LAB4_API_KEY")
    if key_from_request != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
    return key_from_request

# Simulated database for storing activity data
activity_data = [
    {"id": 1, "task": "Complete Lab 4", "description": "Finish assigned laboratory task.", "completed": False}
]

# Pydantic model for handling activity input validation
class ActivityItem(BaseModel):
    task: str
    description: Optional[str] = ""
    completed: bool = False

# Router for version 1 of the API
v1_api_router = APIRouter()

@v1_api_router.get("/tasks/{task_id}")
def fetch_task_v1(task_id: int, api_key: str = Depends(verify_api_key)):
    task = next((t for t in activity_data if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    return task

@v1_api_router.post("/tasks/")
def create_task_v1(task: ActivityItem, api_key: str = Depends(verify_api_key)):
    new_task_id = len(activity_data) + 1
    new_task = task.dict()
    new_task["id"] = new_task_id
    activity_data.append(new_task)
    return JSONResponse(status_code=201, content={"Message": "Task created successfully.", "Task": new_task})

@v1_api_router.patch("/tasks/{task_id}")
def update_task_v1(task_id: int, task: ActivityItem, api_key: str = Depends(verify_api_key)):
    task_to_update = next((t for t in activity_data if t["id"] == task_id), None)
    if not task_to_update:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    for key, value in task.dict(exclude_unset=True).items():
        task_to_update[key] = value
    return JSONResponse(status_code=200, content={"Message": "Task updated successfully.", "Task": task_to_update})

@v1_api_router.delete("/tasks/{task_id}")
def delete_task_v1(task_id: int, api_key: str = Depends(verify_api_key)):
    task_to_delete = next((t for t in activity_data if t["id"] == task_id), None)
    if not task_to_delete:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    activity_data.remove(task_to_delete)
    return JSONResponse(status_code=200, content={"Message": "Task deleted successfully."})

# Router for version 2 of the API
v2_api_router = APIRouter()

@v2_api_router.get("/tasks/{task_id}")
def fetch_task_v2(task_id: int, api_key: str = Depends(verify_api_key)):
    task = next((t for t in activity_data if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    return task

@v2_api_router.post("/tasks/")
def create_task_v2(task: ActivityItem, api_key: str = Depends(verify_api_key)):
    new_task_id = len(activity_data) + 1
    new_task = task.dict()
    new_task["id"] = new_task_id
    activity_data.append(new_task)
    return JSONResponse(status_code=201, content={"Message": "Task created in v2.", "Task": new_task})

@v2_api_router.patch("/tasks/{task_id}")
def update_task_v2(task_id: int, task: ActivityItem, api_key: str = Depends(verify_api_key)):
    task_to_update = next((t for t in activity_data if t["id"] == task_id), None)
    if not task_to_update:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    for key, value in task.dict(exclude_unset=True).items():
        task_to_update[key] = value
    return JSONResponse(status_code=200, content={"Message": "Task updated in v2.", "Task": task_to_update})

@v2_api_router.delete("/tasks/{task_id}")
def delete_task_v2(task_id: int, api_key: str = Depends(verify_api_key)):
    task_to_delete = next((t for t in activity_data if t["id"] == task_id), None)
    if not task_to_delete:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    activity_data.remove(task_to_delete)
    return JSONResponse(status_code=200, content={"Message": "Task deleted in v2."})

# Include versioned API routers
app.include_router(v1_api_router, prefix="/api/v1")
app.include_router(v2_api_router, prefix="/api/v2")

# Root endpoint to confirm the API is running
@app.get("/")
def root():
    return {"Message": "API is up and running. Use /api/v1 or /api/v2 for task management."}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"Status": "API is functional."}
