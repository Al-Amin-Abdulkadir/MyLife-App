# calendar logic for MyLife app
from typing import Any

from sqlalchemy.orm import Session

from app.modules.MyLife_Tracker import ensure_current_user, generate_id, now_dubai
from app.database.models import (
    CalendarEvent as CalendarEventModel,
    Task as TaskModel,
    Project as ProjectModel,
)


def create_calendar_event(
    current_user: dict[str, Any] | None,
    db: Session,
    title: str,
    event_type: str,
    event_date: str,
    notes: str = "",
) -> dict[str, Any] | None:
    current_user = ensure_current_user(current_user)
    if not current_user:
        return None

    event = CalendarEventModel(
        id=generate_id(),
        user_id=current_user["id"],
        title=title.strip() or "untitled",
        event_type=event_type.strip().lower() or "general",
        event_date=event_date,
        notes=notes.strip(),
        created_at=now_dubai(),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return {
        "id": event.id,
        "title": event.title,
        "event_type": event.event_type,
        "event_date": event.event_date,
        "notes": event.notes,
        "created_at": event.created_at,
    }


def list_calendar_events(current_user: dict[str, Any] | None, db: Session) -> list[dict[str, Any]]:
    current_user = ensure_current_user(current_user)
    if not current_user:
        return []
    events = db.query(CalendarEventModel).filter(
        CalendarEventModel.user_id == current_user["id"]
    ).all()
    return [
        {
            "id": e.id,
            "title": e.title,
            "event_type": e.event_type,
            "event_date": e.event_date,
            "notes": e.notes,
            "created_at": e.created_at,
        }
        for e in events
    ]


def group_calendar_events_by_type(current_user: dict[str, Any] | None, db: Session) -> dict[str, int]:
    grouped: dict[str, int] = {}
    for event in list_calendar_events(current_user, db):
        event_type = str(event.get("event_type", "general")).lower()
        grouped[event_type] = grouped.get(event_type, 0) + 1
    return grouped


def list_upcoming_deadlines(current_user: dict[str, Any] | None, db: Session) -> dict[str, list[dict[str, str]]]:
    current_user = ensure_current_user(current_user)
    if not current_user:
        return {"tasks": [], "projects": []}

    user_id = current_user["id"]
    tasks = db.query(TaskModel).filter(
        TaskModel.user_id == user_id,
        TaskModel.task_deadline != "",
        TaskModel.task_deadline.isnot(None),
        TaskModel.is_archived == False,
    ).all()
    projects = db.query(ProjectModel).filter(
        ProjectModel.user_id == user_id,
        ProjectModel.project_deadline != "",
        ProjectModel.project_deadline.isnot(None),
        ProjectModel.is_archived == False,
    ).all()

    return {
        "tasks": [
            {"id": t.id, "name": t.task_name, "deadline": t.task_deadline}
            for t in tasks
        ],
        "projects": [
            {"id": p.id, "name": p.project_title, "deadline": p.project_deadline}
            for p in projects
        ],
    }


def get_calendar_overview(current_user: dict[str, Any] | None, db: Session) -> dict[str, Any] | None:
    current_user = ensure_current_user(current_user)
    if not current_user:
        return None

    user_id = current_user["id"]
    events = db.query(CalendarEventModel).filter(CalendarEventModel.user_id == user_id).all()
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user_id, TaskModel.is_archived == False).all()
    projects = db.query(ProjectModel).filter(ProjectModel.user_id == user_id, ProjectModel.is_archived == False).all()

    events_by_type: dict[str, int] = {}
    for e in events:
        etype = (e.event_type or "general").lower()
        events_by_type[etype] = events_by_type.get(etype, 0) + 1

    deadlines = list_upcoming_deadlines(current_user, db)

    upcoming = sorted(
        [{"title": e.title, "date": e.event_date, "type": e.event_type} for e in events if e.event_date],
        key=lambda x: x["date"],
    )

    return {
        "calendar_events_count": len(events),
        "tasks_count": len(tasks),
        "projects_count": len(projects),
        "events_by_type": events_by_type,
        "upcoming_task_deadlines": deadlines["tasks"],
        "upcoming_project_deadlines": deadlines["projects"],
        "upcoming": upcoming,
    }


def get_reminder_placeholders(current_user: dict[str, Any] | None) -> dict[str, Any]:
    current_user = ensure_current_user(current_user)
    return {
        "current_user_id": str(current_user.get("id")) if current_user else None,
        "status": "not_implemented",
        "message": "Reminder creation and notifications will be implemented through routes/forms.",
    }
