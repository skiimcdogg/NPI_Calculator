from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import TemplateResponse
from typing import Dict
from .service import Services

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/calculate_infix/")
async def perform_calculation(expression: str) -> Dict[str, str]:
    result = Services.calculate_infix_operation(expression)
    return result

@app.post("/calculate_postfix/")
async def perform_calculation(expression: str) -> Dict[str, str]:
    result = Services.calculate_postfix_operation(expression)
    return result

@app.get("/interface/")
async def render_interface(request: Request) -> TemplateResponse:
    return templates.TemplateResponse("interface.html", {"request": request, "message": "Welcome to the RPN Calculator!"})