from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import TEMPLATES_DIR
from app.database import get_db
from app.dependencies import require_user
from app.modules.MyLife_Calender import get_calendar_overview
from app.modules.MyLife_Finance import FinanceSummaryService, AccountService as FinanceAccountService, TransactionService
from app.modules.MyLife_Fitness import CalorieTracker, MealTracker
from app.modules.MyLife_Tracker import (
    HabitService,
    ProductivityOverviewDashboard,
    now_dubai,
    project as TrackerProjectService,
    task as TrackerTaskService,
)
from app.modules.MyLife_statistics import build_statistics_summary
from app.modules.MyLife_Scheduler import ScheduleService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _build_finance_context(current_user, db: Session) -> dict:
    svc = FinanceSummaryService(db)
    txn_svc = TransactionService(db)
    acc_svc = FinanceAccountService(db)
    from datetime import date
    today = date.today()
    year, month = today.year, today.month
    income_month = svc.calculate_total_income_by_month(current_user, year, month)
    expenses_month = svc.calculate_total_expenses_by_month(current_user, year, month)
    net_month = income_month - expenses_month
    total = income_month + expenses_month
    income_pct = round((income_month / total * 100) if total > 0 else 0)
    expense_pct = round((expenses_month / total * 100) if total > 0 else 0)

    accounts = acc_svc.list_accounts(current_user)
    accounts_with_summary = []
    for acc in accounts:
        acc_txns = txn_svc.list_transactions_by_account(current_user, acc["id"])
        inc = sum(float(t["amount"]) for t in acc_txns if t.get("txn_type") == "income")
        exp = sum(float(t["amount"]) for t in acc_txns if t.get("txn_type") == "expense")
        accounts_with_summary.append({**acc, "income": inc, "expenses": exp, "net": inc - exp})

    base = svc.build_finance_summary(current_user)
    base.update({
        "income_month": income_month,
        "expenses_month": expenses_month,
        "net_month": net_month,
        "income_pct": income_pct,
        "expense_pct": expense_pct,
        "balance": base.get("net_balance", 0),
        "accounts_with_summary": accounts_with_summary,
    })
    return base


def _build_dashboard_context(current_user, db: Session):
    task_service = TrackerTaskService(db)
    habit_service = HabitService(db)
    project_service = TrackerProjectService(db)
    productivity_dashboard = ProductivityOverviewDashboard()

    tasks = task_service.view_tasks(current_user)
    habits = habit_service.list_habits(current_user)
    projects = project_service.show_projects(current_user)

    today = now_dubai().split("T")[0]
    calorie_tracker = CalorieTracker(db)
    all_meals = MealTracker(db).view_meal(current_user)
    meals_today = [m for m in all_meals if m.get("completion_date") == today]

    return {
        "tasks": tasks,
        "habits": habits,
        "projects": projects,
        "tracker": {
            "tasks": productivity_dashboard.task_metrics(tasks),
            "habits": productivity_dashboard.habits_metrics(habits),
            "projects": productivity_dashboard.projects_metrics(projects),
        },
        "finance": _build_finance_context(current_user, db),
        "fitness": calorie_tracker.show_daily_calorie(current_user, today),
        "meals_today": meals_today,
        "calendar": get_calendar_overview(current_user, db) or {},
        "statistics": build_statistics_summary(current_user, db) or {},
        "schedules": ScheduleService(db).list_schedules(current_user),
        "today": today,
    }


@router.get("", response_class=HTMLResponse)
def dashboard_home(
    request: Request,
    current_user=Depends(require_user),
    db: Session = Depends(get_db),
):
    dashboard = _build_dashboard_context(current_user, db)

    return templates.TemplateResponse(
        "dashboard/dashboard.html",
        {
            "request": request,
            "current_user": current_user,
            "dashboard": dashboard,
            "error": None,
        },
    )


@router.get("/", response_class=HTMLResponse)
def dashboard_home_slash(
    request: Request,
    current_user=Depends(require_user),
    db: Session = Depends(get_db),
):
    return dashboard_home(request, current_user, db)


@router.get("/overview", response_class=HTMLResponse)
def dashboard_overview(
    request: Request,
    current_user=Depends(require_user),
    db: Session = Depends(get_db),
):
    dashboard = _build_dashboard_context(current_user, db)

    return templates.TemplateResponse(
        "dashboard/overview.html",
        {
            "request": request,
            "current_user": current_user,
            "dashboard": dashboard,
            "error": None,
        },
    )


@router.get("/quick-links", response_class=HTMLResponse)
def dashboard_quick_links(request: Request, current_user=Depends(require_user)):
    links = [
        {"label": "Tracker", "url": "/tracker/dashboard"},
        {"label": "Finance", "url": "/finance/dashboard"},
        {"label": "Fitness", "url": "/fitness/dashboard"},
        {"label": "Calendar", "url": "/calendar/dashboard"},
        {"label": "Scheduler", "url": "/scheduler/dashboard"},
        {"label": "Statistics", "url": "/statistics/dashboard"},
    ]

    return templates.TemplateResponse(
        "dashboard/quick_links.html",
        {
            "request": request,
            "current_user": current_user,
            "links": links,
            "error": None,
        },
    )
