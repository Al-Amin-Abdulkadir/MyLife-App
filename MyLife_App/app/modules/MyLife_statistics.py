from typing import Any

from sqlalchemy.orm import Session

from app.modules.MyLife_Tracker import ensure_current_user, now_dubai
from app.modules.MyLife_Calender import get_calendar_overview
from app.database.models import (
    Task as TaskModel,
    Habit as HabitModel,
    Project as ProjectModel,
)


def _build_fitness_statistics(current_user: dict[str, Any] | None) -> dict[str, int]:
    return {}


def _build_finance_statistics(current_user: dict[str, Any] | None) -> dict[str, int]:
    return {}


def build_statistics_summary(current_user: dict[str, Any] | None, db: Session) -> dict[str, Any] | None:
    current_user = ensure_current_user(current_user)
    if not current_user:
        return None

    user_id = current_user["id"]
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user_id, TaskModel.is_archived == False).all()
    habits = db.query(HabitModel).filter(HabitModel.user_id == user_id, HabitModel.is_archived == False).all()
    projects = db.query(ProjectModel).filter(ProjectModel.user_id == user_id, ProjectModel.is_archived == False).all()

    return {
        "tasks_tracked": len(tasks),
        "habits_tracked": len(habits),
        "projects_tracked": len(projects),
        "fitness": _build_fitness_statistics(current_user),
        "finance": _build_finance_statistics(current_user),
        "calendar": get_calendar_overview(current_user, db) or {},
    }


def build_productivity_analytics(current_user: dict[str, Any] | None, db: Session) -> dict[str, Any] | None:
    current_user = ensure_current_user(current_user)
    if not current_user:
        return None

    user_id = current_user["id"]
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user_id, TaskModel.is_archived == False).all()
    projects = db.query(ProjectModel).filter(ProjectModel.user_id == user_id, ProjectModel.is_archived == False).all()

    return {
        "tasks_total": len(tasks),
        "tasks_completed": len([t for t in tasks if t.status == "completed"]),
        "projects_total": len(projects),
        "projects_completed": len([p for p in projects if p.status == "completed"]),
    }


def build_habit_analytics(current_user: dict[str, Any] | None, db: Session) -> dict[str, Any] | None:
    current_user = ensure_current_user(current_user)
    if not current_user:
        return None

    today = now_dubai()[:10]
    habits = db.query(HabitModel).filter(
        HabitModel.user_id == current_user["id"],
        HabitModel.is_archived == False,
    ).all()
    return {
        "habits_total": len(habits),
        "habits_completed_today": len([h for h in habits if h.last_completed_date == today]),
    }


def build_finance_analytics(current_user: dict[str, Any] | None) -> dict[str, int]:
    return _build_finance_statistics(current_user)
