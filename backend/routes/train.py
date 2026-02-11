from fastapi import APIRouter
from fastapi.responses import Response

from src.pipeline import TrainPipeline

router = APIRouter()


@router.get("/train")
async def train_route():
    try:
        pipeline = TrainPipeline()
        pipeline.run_pipeline()
        return Response("Training successful!")
    except Exception as e:
        return Response(f"Error: {e}")
