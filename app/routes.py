from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.responses import TemplateResponse
from .service import Services

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/calculate-infix/")
async def perform_calculation_infix(expression: str = Form(...)) -> RedirectResponse:
    try:
        result = Services.calculate_infix_operation(expression)
        return RedirectResponse(url=f"/interface/?message=Infix calculation result: {result['result']}")
    except Exception as e:
        return RedirectResponse(url=f"/interface/?message=Error in Infix calculation: {str(e)}")

@router.post("/calculate-postfix/")
async def perform_calculation_postfix(expression: str = Form(...)) -> RedirectResponse:
    try:
        result = Services.calculate_postfix_operation(expression)
        return RedirectResponse(url=f"/interface/?message=Postfix calculation result: {result['result']}")
    except Exception as e:
        return RedirectResponse(url=f"/interface/?message=Error in Postfix calculation: {str(e)}")

@router.get("/export-csv-data/")
async def get_csv_data_from_db(request: Request) -> RedirectResponse:
    try:
        result = Services.get_csv_data_from_db()
        return RedirectResponse(url=f"/interface/?message=Data exported successfully")
    except Exception as e:
        return RedirectResponse(url=f"/interface/?message=Error during exporting data: {str(e)}")

@router.get("/interface/")
async def render_interface(request: Request, message: str = "") -> TemplateResponse:
    return templates.TemplateResponse("interface.html", {"request": request, "message": message})