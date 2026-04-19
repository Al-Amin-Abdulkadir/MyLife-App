from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.modules.MyLife_Tracker import get_current_user_from_token


def get_current_user(request : Request, db : Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    return get_current_user_from_token(token, db)


def require_user(current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated"
        )
    return current_user