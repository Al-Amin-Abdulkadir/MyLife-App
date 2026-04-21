from app.modules.MyLife_Tracker import ensure_current_user, generate_id, now_dubai
from sqlalchemy.orm import Session
from app.database.models import (
    Schedule as ScheduleModel,
    ScheduledActivity as ActivityModel,
)


def _schedule_to_dict(s: ScheduleModel) -> dict:
    return {
        "id": s.id,
        "user_id": s.user_id,
        "name": s.name,
        "description": s.description or "",
        "created_at": s.created_at or "",
        "updated_at": s.updated_at or "",
    }


def _activity_to_dict(a: ActivityModel) -> dict:
    return {
        "id": a.id,
        "user_id": a.user_id,
        "schedule_id": a.schedule_id,
        "activity_name": a.activity_name,
        "date": a.date or "",
        "start_time": a.start_time or "",
        "end_time": a.end_time or "",
    }


class ScheduleService:
    def __init__(self, db: Session):
        self.db = db

    def create_schedule(self, current_user, name: str, description: str = ""):
        current_user = ensure_current_user(current_user)
        if not current_user:
            return None

        u_id = str(current_user.get("id"))

        exists = self.db.query(ScheduleModel).filter(
            ScheduleModel.user_id == u_id,
            ScheduleModel.name.ilike(name.strip()),
        ).first()

        if exists:
            raise ValueError("A schedule with this name already exists")

        schedule = ScheduleModel(
            id=generate_id(),
            user_id=u_id,
            name=name.strip(),
            description=description or "",
            created_at=now_dubai(),
            updated_at=now_dubai(),
        )
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        return _schedule_to_dict(schedule)

    def list_schedules(self, current_user):
        current_user = ensure_current_user(current_user)
        if not current_user:
            return []

        u_id = str(current_user.get("id"))
        records = self.db.query(ScheduleModel).filter(
            ScheduleModel.user_id == u_id
        ).order_by(ScheduleModel.created_at).all()

        return [_schedule_to_dict(r) for r in records]

    def get_schedule_by_id(self, current_user, schedule_id: str):
        current_user = ensure_current_user(current_user)
        if not current_user:
            return None

        record = self.db.query(ScheduleModel).filter(
            ScheduleModel.user_id == str(current_user.get("id")),
            ScheduleModel.id == schedule_id,
        ).first()

        return _schedule_to_dict(record) if record else None

    def edit_schedule(self, current_user, schedule_id: str, updated_name: str, updated_description: str = ""):
        current_user = ensure_current_user(current_user)
        if not current_user:
            return None

        u_id = str(current_user.get("id"))

        duplicate = self.db.query(ScheduleModel).filter(
            ScheduleModel.user_id == u_id,
            ScheduleModel.name.ilike(updated_name.strip()),
            ScheduleModel.id != schedule_id,
        ).first()

        if duplicate:
            raise ValueError("A schedule with this name already exists")

        record = self.db.query(ScheduleModel).filter(
            ScheduleModel.user_id == u_id,
            ScheduleModel.id == schedule_id,
        ).first()

        if not record:
            return None

        record.name = updated_name.strip()
        record.description = updated_description or ""
        record.updated_at = now_dubai()
        self.db.commit()
        return _schedule_to_dict(record)

    def delete_schedule(self, current_user, schedule_id: str):
        current_user = ensure_current_user(current_user)
        if not current_user:
            return False

        u_id = str(current_user.get("id"))

        record = self.db.query(ScheduleModel).filter(
            ScheduleModel.user_id == u_id,
            ScheduleModel.id == schedule_id,
        ).first()

        if not record:
            return False

        self.db.delete(record)
        self.db.commit()
        return True


class ActivityService:
    def __init__(self, db: Session):
        self.db = db

    def add_activity(
        self,
        current_user,
        schedule_id: str,
        activity_name: str,
        date: str,
        start_time: str,
        end_time: str,
    ):
        current_user = ensure_current_user(current_user)
        if not current_user:
            return None

        u_id = str(current_user.get("id"))

        schedule = self.db.query(ScheduleModel).filter(
            ScheduleModel.user_id == u_id,
            ScheduleModel.id == schedule_id,
        ).first()

        if not schedule:
            return None

        activity = ActivityModel(
            id=generate_id(),
            user_id=u_id,
            schedule_id=schedule_id,
            activity_name=activity_name.strip(),
            date=date,
            start_time=start_time,
            end_time=end_time,
        )

        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return _activity_to_dict(activity)

    def list_activities(self, current_user, schedule_id: str):
        current_user = ensure_current_user(current_user)
        if not current_user:
            return []

        u_id = str(current_user.get("id"))

        records = self.db.query(ActivityModel).filter(
            ActivityModel.user_id == u_id,
            ActivityModel.schedule_id == schedule_id,
        ).order_by(ActivityModel.date, ActivityModel.start_time).all()

        return [_activity_to_dict(r) for r in records]

    def get_activity_by_id(self, current_user, activity_id: str):
        current_user = ensure_current_user(current_user)
        if not current_user:
            return None

        record = self.db.query(ActivityModel).filter(
            ActivityModel.user_id == str(current_user.get("id")),
            ActivityModel.id == activity_id,
        ).first()

        return _activity_to_dict(record) if record else None

    def edit_activity(
        self,
        current_user,
        activity_id: str,
        activity_name: str,
        date: str,
        start_time: str,
        end_time: str,
    ):
        current_user = ensure_current_user(current_user)
        if not current_user:
            return None

        record = self.db.query(ActivityModel).filter(
            ActivityModel.user_id == str(current_user.get("id")),
            ActivityModel.id == activity_id,
        ).first()

        if not record:
            return None

        record.activity_name = activity_name.strip()
        record.date = date
        record.start_time = start_time
        record.end_time = end_time
        self.db.commit()
        return _activity_to_dict(record)

    def delete_activity(self, current_user, activity_id: str):
        current_user = ensure_current_user(current_user)
        if not current_user:
            return False

        record = self.db.query(ActivityModel).filter(
            ActivityModel.user_id == str(current_user.get("id")),
            ActivityModel.id == activity_id,
        ).first()

        if not record:
            return False

        self.db.delete(record)
        self.db.commit()
        return True
