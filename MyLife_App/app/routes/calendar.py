from fastapi import APIRouter

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/")
def calendar_home():
    return {"message": "Calendar routes scaffolded"}

