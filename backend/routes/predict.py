from fastapi import APIRouter, Request

from backend.config import templates
from backend.forms.vehicle_form import DataForm
from backend.services import PredictionService

router = APIRouter()


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "vehicledata.html",
        {"request": request, "context": "Rendering"},
    )


@router.post("/")
async def predict(request: Request):
    try:
        form = DataForm(request)
        await form.load_data()

        result = PredictionService.predict(form)

        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "context": result},
        )

    except Exception as e:
        return {"status": False, "error": str(e)}
