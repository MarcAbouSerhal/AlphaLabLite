from fastapi import FastAPI, Query
from pydantic import BaseModel
from services import *
from utils import *

app = FastAPI()

class ExecuteRequest(BaseModel):
    script: str


@app.post("/execute")
def execute_endpoint(request: ExecuteRequest):
    lines = [remove_whitespace(line) for line in request.script.splitlines()]
    id = execute(lines)
    return {"message": "Script successfully executed", "result": id}


@app.get("/view/{id}")
def view_endpoint(id: str, items: list[str] = Query(default=[])):
    series = view(id, items)
    return series