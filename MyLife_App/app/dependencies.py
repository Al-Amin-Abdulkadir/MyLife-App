from app.modules.MyLife_Tracker import ensure_current_user


def get_current_user(current_user=None):
    return ensure_current_user(current_user)
