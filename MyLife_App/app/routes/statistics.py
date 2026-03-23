from fastapi import APIRouter

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/")
def statistics_home():
    return {"message": "Statistics routes scaffolded"}

