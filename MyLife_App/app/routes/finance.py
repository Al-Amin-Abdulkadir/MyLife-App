from fastapi import APIRouter

router = APIRouter(prefix="/finance", tags=["finance"])


@router.get("/")
def finance_home():
    return {"message": "Finance routes scaffolded"}

