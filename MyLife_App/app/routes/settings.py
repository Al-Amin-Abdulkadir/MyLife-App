from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import TEMPLATES_DIR
from app.database import get_db
from app.dependencies import require_user
from app.modules.MyLife_Tracker import AccountService as AuthService

router = APIRouter(prefix="/settings", tags=["settings"])
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("", response_class=HTMLResponse)
def settins_page(request : Request, current_user=Depends(require_user)):
    return templates.TemplateResponse(
        "settings/index.html",
        {
            "request" : request,
            "current_user" : current_user,
            "success" : None,
            "error" : None,
        }
    )

@router.post("/change-password", response_class=HTMLResponse)
def change_password(
    request : Request,
    current_password : str =Form(...),
    new_password : str = Form(...),
    confirm_password : str = Form(...),
    current_user=Depends(require_user),
    db : Session = Depends(get_db),
):
    if new_password != confirm_password:
        return templates.TemplateResponse(
            "settings/index.html",
            {
                "request" : request,
                "current_user" : current_user,
                "error" : "New passwords do not match",
                "success": None,
            },
            status_code=400
        )
    try:
        result = AuthService(db).change_password(current_user, current_password, new_password)
    except ValueError as exc:
        return templates.TemplateResponse(
            "settings/index.html",
            {"request": request, "current_user": current_user, "error": str(exc), "success": None},
            status_code=400,
        )
    if not result:
        return templates.TemplateResponse(
            "settings/index.html",
            {"request": request, "current_user": current_user, "error": "Current password is incorrect.", "success": None},
            status_code=400,
        )
    return templates.TemplateResponse(
        "settings/index.html",
        {
            "request" : request,
            "current_user" : current_user,
            "success" : "Password changed successfully.", 
            "error" : None
        },

    )