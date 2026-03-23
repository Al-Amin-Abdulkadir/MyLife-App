from fastapi import APIRouter

router = APIRouter(prefix="/tracker", tags=["tracker"])


@router.get("/")
def tracker_home():
    return {"message": "Tracker routes scaffolded"}

