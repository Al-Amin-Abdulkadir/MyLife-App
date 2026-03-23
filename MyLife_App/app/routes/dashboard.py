from fastapi import APIRouter

router = APIRouter(tags=["dashboard"])


@router.get("/")
def dashboard_home():
    return {"message": "MyLife web app scaffold is ready"}

