from fastapi import APIRouter

router = APIRouter(prefix="/fitness", tags=["fitness"])


@router.get("/")
def fitness_home():
    return {"message": "Fitness routes scaffolded"}

