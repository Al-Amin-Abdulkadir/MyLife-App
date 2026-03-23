from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR
from app.routes.auth import router as auth_router
from app.routes.calendar import router as calendar_router
from app.routes.dashboard import router as dashboard_router
from app.routes.finance import router as finance_router
from app.routes.fitness import router as fitness_router
from app.routes.statistics import router as statistics_router
from app.routes.tracker import router as tracker_router

app = FastAPI(title="MyLife Web App")

app.include_router(dashboard_router)
app.include_router(auth_router)
app.include_router(tracker_router)
app.include_router(calendar_router)
app.include_router(finance_router)
app.include_router(fitness_router)
app.include_router(statistics_router)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

