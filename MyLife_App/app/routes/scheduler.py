from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import TEMPLATES_DIR
from app.database import get_db
from app.dependencies import require_user
from app.modules.MyLife_Scheduler import ActivityService, ScheduleService

router = APIRouter(prefix="/scheduler", tags=["scheduler"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# ── Schedules ────────────────────────────────────────────────────────────────

@router.get("/dashboard", response_class=HTMLResponse)
def scheduler_dashboard(
    request: Request,
    current_user=Depends(require_user),
    db: Session = Depends(get_db),
):
    schedules = ScheduleService(db).list_schedules(current_user)
    return templates.TemplateResponse(
        "scheduler/dashboard.html",
        {"request": request, "current_user": current_user, "schedules": schedules},
    )


@router.get("/new", response_class=HTMLResponse)
def create_schedule_page(request: Request, current_user=Depends(require_user)):
    return templates.TemplateResponse(
        "scheduler/create_schedule.html",
        {"request": request, "current_user": current_user, "error": None},
    )


@router.post("/new", response_class=HTMLResponse)
def create_schedule_submit(
    request: Request,
    current_user=Depends(require_user),
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        ScheduleService(db).create_schedule(current_user, name, description)
    except ValueError as exc:
        return templates.TemplateResponse(
            "scheduler/create_schedule.html",
            {"request": request, "current_user": current_user, "error": str(exc)},
            status_code=400,
        )
    return RedirectResponse(url="/scheduler/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{schedule_id}", response_class=HTMLResponse)
def view_schedule(
    request: Request,
    schedule_id: str,
    current_user=Depends(require_user),
    db: Session = Depends(get_db),
):
    svc = ScheduleService(db)
    schedule = svc.get_schedule_by_id(current_user, schedule_id)
    if not schedule:
        return RedirectResponse(url="/scheduler/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    activities = ActivityService(db).list_activities(current_user, schedule_id)
    return templates.TemplateResponse(
        "scheduler/view_schedule.html",
        {
            "request": request,
            "current_user": current_user,
            "schedule": schedule,
            "activities": activities,
        },
    )


@router.get("/{schedule_id}/edit", response_class=HTMLResponse)
def edit_schedule_page(
    request: Request,
    schedule_id: str,
    current_user=Depends(require_user),
    db: Session = Depends(get_db),
):
    schedule = ScheduleService(db).get_schedule_by_id(current_user, schedule_id)
    if not schedule:
        return RedirectResponse(url="/scheduler/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(
        "scheduler/edit_schedule.html",
        {"request": request, "current_user": current_user, "schedule": schedule, "error": None},
    )


@router.post("/{schedule_id}/edit", response_class=HTMLResponse)
def edit_schedule_submit(
    request: Request,
    schedule_id: str,
    current_user=Depends(require_user),
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        ScheduleService(db).edit_schedule(current_user, schedule_id, name, description)
    except ValueError as exc:
        schedule = ScheduleService(db).get_schedule_by_id(current_user, schedule_id)
        return templates.TemplateResponse(
            "scheduler/edit_schedule.html",
            {"request": request, "current_user": current_user, "schedule": schedule, "error": str(exc)},
            status_code=400,
        )
    return RedirectResponse(url=f"/scheduler/{schedule_id}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{schedule_id}/delete")
def delete_schedule(
    schedule_id: str,
    current_user=Depends(require_user),
    db: Session = Depends(get_db),
):
    ScheduleService(db).delete_schedule(current_user, schedule_id)
    return RedirectResponse(url="/scheduler/dashboard", status_code=status.HTTP_303_SEE_OTHER)



@router.get("/{schedule_id}/add-activity", response_class=HTMLResponse)
def add_activity_page(
    request: Request,
    schedule_id: str,
    current_user=Depends(require_user),
    db: Session = Depends(get_db),
):
    schedule = ScheduleService(db).get_schedule_by_id(current_user, schedule_id)
    if not schedule:
        return RedirectResponse(url="/scheduler/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(
        "scheduler/add_activity.html",
        {"request": request, "current_user": current_user, "schedule": schedule, "error": None},
    )


@router.post("/{schedule_id}/add-activity", response_class=HTMLResponse)
def add_activity_submit(
    request: Request,
    schedule_id: str,
    current_user=Depends(require_user),
    activity_name: str = Form(...),
    date: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        ActivityService(db).add_activity(
            current_user, schedule_id, activity_name, date, start_time, end_time
        )
    except ValueError as exc:
        schedule = ScheduleService(db).get_schedule_by_id(current_user, schedule_id)
        return templates.TemplateResponse(
            "scheduler/add_activity.html",
            {"request": request, "current_user": current_user, "schedule": schedule, "error": str(exc)},
            status_code=400,
        )
    return RedirectResponse(url=f"/scheduler/{schedule_id}", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{schedule_id}/activities/{activity_id}/edit", response_class=HTMLResponse)
def edit_activity_page(
    request: Request,
    schedule_id: str,
    activity_id: str,
    current_user=Depends(require_user),
    db: Session = Depends(get_db),
):
    schedule = ScheduleService(db).get_schedule_by_id(current_user, schedule_id)
    activity = ActivityService(db).get_activity_by_id(current_user, activity_id)
    if not schedule or not activity:
        return RedirectResponse(url=f"/scheduler/{schedule_id}", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(
        "scheduler/edit_activity.html",
        {
            "request": request,
            "current_user": current_user,
            "schedule": schedule,
            "activity": activity,
            "error": None,
        },
    )


@router.post("/{schedule_id}/activities/{activity_id}/edit", response_class=HTMLResponse)
def edit_activity_submit(
    request: Request,
    schedule_id: str,
    activity_id: str,
    current_user=Depends(require_user),
    activity_name: str = Form(...),
    date: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        ActivityService(db).edit_activity(
            current_user, activity_id, activity_name, date, start_time, end_time
        )
    except ValueError as exc:
        schedule = ScheduleService(db).get_schedule_by_id(current_user, schedule_id)
        activity = ActivityService(db).get_activity_by_id(current_user, activity_id)
        return templates.TemplateResponse(
            "scheduler/edit_activity.html",
            {
                "request": request,
                "current_user": current_user,
                "schedule": schedule,
                "activity": activity,
                "error": str(exc),
            },
            status_code=400,
        )
    return RedirectResponse(url=f"/scheduler/{schedule_id}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{schedule_id}/activities/{activity_id}/delete")
def delete_activity(
    schedule_id: str,
    activity_id: str,
    current_user=Depends(require_user),
    db: Session = Depends(get_db),
):
    ActivityService(db).delete_activity(current_user, activity_id)
    return RedirectResponse(url=f"/scheduler/{schedule_id}", status_code=status.HTTP_303_SEE_OTHER)
