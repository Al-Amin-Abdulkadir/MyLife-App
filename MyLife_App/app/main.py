from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import STATIC_DIR, TEMPLATES_DIR
from app.routes.auth import auth_router
from app.routes.calendar import router as calendar_router
from app.routes.dashboard import router as dashboard_router
from app.routes.finance import router as finance_router
from app.routes.fitness import router as fitness_router
from app.routes.statistics import router as statistics_router
from app.routes.tracker import router as tracker_router
from app.routes.settings import router as settings_router
from app.routes.home import router as home_router
from app.routes.scheduler import router as scheduler_router

app = FastAPI(title="MyLife Web App")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return templates.TemplateResponse(
            "auth/session_expired.html",
            {"request": request},
            status_code=401,
        )
    raise exc

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(tracker_router)
app.include_router(finance_router)
app.include_router(fitness_router)
app.include_router(calendar_router)
app.include_router(statistics_router)
app.include_router(settings_router)
app.include_router(home_router)
app.include_router(scheduler_router)




