from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import TEMPLATES_DIR
from app.dependencies import require_user
from app.modules.MyLife_statistics import (
    build_finance_analytics,
    build_habit_analytics,
    build_productivity_analytics,
    build_statistics_summary,
    _build_fitness_statistics,
)

router = APIRouter(prefix="/statistics", tags=["statistics"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/dashboard", response_class=HTMLResponse)
def statistics_dashboard(request: Request, current_user=Depends(require_user)):
    summary = build_statistics_summary(current_user)
    productivity = build_productivity_analytics(current_user)
    habits = build_habit_analytics(current_user)
    finance = build_finance_analytics(current_user)
    fitness = _build_fitness_statistics(current_user)

    return templates.TemplateResponse(
        "statistics/dashboard.html",
        {
            "request": request,
            "current_user": current_user,
            "summary": summary or {},
            "productivity": productivity or {},
            "habits": habits or {},
            "finance": finance or {},
            "fitness": fitness or {},
            "error": None,
        },
    )


@router.get("/summary", response_class=HTMLResponse)
def statistics_summary_page(request: Request, current_user=Depends(require_user)):
    summary = build_statistics_summary(current_user)

    return templates.TemplateResponse(
        "statistics/summary.html",
        {
            "request": request,
            "current_user": current_user,
            "summary": summary or {},
            "error": None,
        },
    )


@router.get("/productivity", response_class=HTMLResponse)
def productivity_statistics_page(request: Request, current_user=Depends(require_user)):
    productivity = build_productivity_analytics(current_user)

    return templates.TemplateResponse(
        "statistics/productivity.html",
        {
            "request": request,
            "current_user": current_user,
            "productivity": productivity or {},
            "error": None,
        },
    )


@router.get("/habits", response_class=HTMLResponse)
def habit_statistics_page(request: Request, current_user=Depends(require_user)):
    habits = build_habit_analytics(current_user)

    return templates.TemplateResponse(
        "statistics/habits.html",
        {
            "request": request,
            "current_user": current_user,
            "habits": habits or {},
            "error": None,
        },
    )


@router.get("/finance", response_class=HTMLResponse)
def finance_statistics_page(request: Request, current_user=Depends(require_user)):
    finance = build_finance_analytics(current_user)

    return templates.TemplateResponse(
        "statistics/finance.html",
        {
            "request": request,
            "current_user": current_user,
            "finance": finance or {},
            "error": None,
        },
    )


@router.get("/fitness", response_class=HTMLResponse)
def fitness_statistics_page(request: Request, current_user=Depends(require_user)):
    fitness = _build_fitness_statistics(current_user)

    return templates.TemplateResponse(
        "statistics/fitness.html",
        {
            "request": request,
            "current_user": current_user,
            "fitness": fitness or {},
            "error": None,
        },
    )
