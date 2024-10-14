from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse
from .service import Services

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/calculate-infix/")
async def perform_calculation_infix(expression: str = Form(...)) -> RedirectResponse:
    try:
        result = await Services.calculate_infix_operation(expression)
        return RedirectResponse(url=f"/interface/?message=Infix calculation result: {result['result']}", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/interface/?message=Error in Infix calculation: {str(e)}", status_code=303)

@router.post("/calculate-postfix/")
async def perform_calculation_postfix(expression: str = Form(...)) -> RedirectResponse:
    try:
        result = await Services.calculate_postfix_operation(expression)
        return RedirectResponse(url=f"/interface/?message=Postfix calculation result: {result['result']}", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/interface/?message=Error in Postfix calculation: {str(e)}", status_code=303)

@router.get("/export-csv-data/")
async def get_csv_data_from_db(request: Request) -> RedirectResponse:
    try:
        file_path = await Services.get_csv_data_from_db()
        return FileResponse(path=file_path, filename="exported_data.csv", media_type='application/csv')
        # -------------------------------------------
        # FOR TESTING LOCAL WITHOUT DOCKER ENVIRONMENT
        # result = Services.get_csv_data_from_db()
        # return RedirectResponse(url=f"/interface/?message=Data exported successfully")
        # -----------------------------------------
    except Exception as e:
        return RedirectResponse(url=f"/interface/?message=Error during exporting data: {str(e)}", status_code=303)

@router.get("/interface/")
async def render_interface(request: Request, message: str = ""):
    return templates.TemplateResponse("interface.html", {"request": request, "message": message})