from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.config import TEMPLATES_DIR
from app.dependencies import require_user
from app.modules.MyLife_Calender import (
    create_calendar_event,
    get_calendar_overview,
    get_reminder_placeholders,
    group_calendar_events_by_type,
    list_calendar_events,
    list_upcoming_deadlines,
)

router = APIRouter(prefix="/calendar", tags=["calendar"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/dashboard", response_class=HTMLResponse)
def calendar_dashboard_page(request: Request, current_user=Depends(require_user)):
    overview = get_calendar_overview(current_user)

    return templates.TemplateResponse(
        "calendar/dashboard.html",
        {
            "request": request,
            "current_user": current_user,
            "overview": overview or {},
            "error": None,
        },
    )


@router.get("/events", response_class=HTMLResponse)
def create_event_page(request: Request, current_user=Depends(require_user)):
    return templates.TemplateResponse(
        "calendar/create_event.html",
        {
            "request": request,
            "current_user": current_user,
            "error": None,
        },
    )


@router.post("/events", response_class=HTMLResponse)
def create_event_submit(
    request: Request,
    title: str = Form(...),
    event_type: str = Form(...),
    event_date: str = Form(...),
    notes: str = Form(""),
    current_user=Depends(require_user),
):
    event = create_calendar_event(
        current_user=current_user,
        title=title,
        event_type=event_type,
        event_date=event_date,
        notes=notes,
    )

    if not event:
        return templates.TemplateResponse(
            "calendar/create_event.html",
            {
                "request": request,
                "current_user": current_user,
                "event": {
                    "title": title,
                    "event_type": event_type,
                    "event_date": event_date,
                    "notes": notes,
                },
                "error": "Unable to create calendar event.",
            },
            status_code=400,
        )

    return RedirectResponse(
        url="/calendar/events/list",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/events/list", response_class=HTMLResponse)
def events_list_page(request: Request, current_user=Depends(require_user)):
    events = list_calendar_events(current_user)

    return templates.TemplateResponse(
        "calendar/events_list.html",
        {
            "request": request,
            "current_user": current_user,
            "events": events,
            "error": None,
        },
    )


@router.get("/overview", response_class=HTMLResponse)
def calendar_overview_page(request: Request, current_user=Depends(require_user)):
    overview = get_calendar_overview(current_user)

    return templates.TemplateResponse(
        "calendar/overview.html",
        {
            "request": request,
            "current_user": current_user,
            "overview": overview or {},
            "error": None,
        },
    )


@router.get("/events/by-type", response_class=HTMLResponse)
def events_by_type_page(request: Request, current_user=Depends(require_user)):
    events_by_type = group_calendar_events_by_type(current_user)

    return templates.TemplateResponse(
        "calendar/events_by_type.html",
        {
            "request": request,
            "current_user": current_user,
            "events_by_type": events_by_type,
            "error": None,
        },
    )


@router.get("/deadlines", response_class=HTMLResponse)
def deadlines_page(request: Request, current_user=Depends(require_user)):
    deadlines = list_upcoming_deadlines(current_user)

    return templates.TemplateResponse(
        "calendar/deadlines.html",
        {
            "request": request,
            "current_user": current_user,
            "deadlines": deadlines,
            "task_deadlines": deadlines.get("tasks", []),
            "project_deadlines": deadlines.get("projects", []),
            "error": None,
        },
    )


@router.get("/reminders", response_class=HTMLResponse)
def reminders_page(request: Request, current_user=Depends(require_user)):
    reminders = get_reminder_placeholders(current_user)

    return templates.TemplateResponse(
        "calendar/reminders.html",
        {
            "request": request,
            "current_user": current_user,
            "reminders": reminders,
            "error": None,
        },
    )
