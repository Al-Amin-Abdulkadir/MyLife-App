from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import TEMPLATES_DIR
from app.dependencies import get_current_user

router = APIRouter(tags=["home"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
def landing_page(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "home/MyLife_Home.html",
        {"request": request, "current_user": current_user},
    )


@router.get("/about", response_class=HTMLResponse)
def about_page(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "home/MyLife_about.html",
        {"request": request, "current_user": current_user},
    )


@router.get("/services", response_class=HTMLResponse)
def services_page(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "home/Mylife_sevices.html",
        {"request": request, "current_user": current_user},
    )
