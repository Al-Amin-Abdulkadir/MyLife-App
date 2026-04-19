import logging
from typing import Any

from sqlalchemy.orm import Session

from app.database.models import (
    Meal as MealModel,
    MealPlan as MealPlanModel,
    Routine as RoutineModel,
    User as UserModel,
    WorkoutSession as WorkoutSessionModel,
)
from app.modules.MyLife_Tracker import (
    ensure_current_user,
    generate_id,
    now_dubai,
    validate_date_input,
)

logger = logging.getLogger("mylife_fitness")


def _current_user_id(current_user: dict | None) -> str | None:
    current_user = ensure_current_user(current_user)
    if not current_user:
        return None
    return str(current_user.get("id"))


def _meal_to_dict(m: MealModel) -> dict[str, Any]:
    return {
        "id": m.id,
        "user_id": m.user_id,
        "meal_name": m.meal_name,
        "meal": m.meal_name,
        "meal_type": m.meal_type,
        "calories": m.calories or 0,
        "protein": m.protein or 0,
        "carbs": m.carbs or 0,
        "fats": m.fats or 0,
        "completion_date": m.completion_date or "",
        "time_of_log": m.time_of_log or "",
        "notes": m.notes or "",
    }


def _meal_plan_to_dict(p: MealPlanModel) -> dict[str, Any]:
    return {
        "id": p.id,
        "user_id": p.user_id,
        "plan_name": p.plan_name,
        "goal": p.goal or "",
        "daily_target_calories": p.daily_target_calories or 0,
        "daily_target_protein": p.daily_target_protein or 0,
        "daily_target_carbs": p.daily_target_carbs or 0,
        "daily_target_fats": p.daily_target_fats or 0,
        "meals": p.meals or [],
        "created_at": p.created_at or "",
        "updated_at": p.updated_at or "",
    }


def _workout_to_dict(w: WorkoutSessionModel) -> dict[str, Any]:
    return {
        "id": w.id,
        "user_id": w.user_id,
        "name": w.name,
        "blocks": w.blocks or [],
        "notes": w.notes or "",
        "created_at": w.created_at or "",
        "updated_at": w.updated_at or "",
    }


def _routine_to_dict(r: RoutineModel) -> dict[str, Any]:
    return {
        "id": r.id,
        "user_id": r.user_id,
        "name": r.name,
        "days": r.days or [],
        "created_at": r.created_at or "",
        "updated_at": r.updated_at or "",
    }


class CalorieTracker:
    def __init__(self, db: Session):
        self.db = db

    def set_calorie_goal(self, current_user: dict | None, goal: int) -> None:
        uid = _current_user_id(current_user)
        if not uid:
            raise ValueError("Current user not found")
        user = self.db.query(UserModel).filter(UserModel.id == uid).first()
        if not user:
            raise ValueError("Current user not found")
        user.daily_calorie_goal = int(goal)
        self.db.commit()

    def get_daily_calorie_goal(self, current_user: dict | None) -> int:
        uid = _current_user_id(current_user)
        if not uid:
            return 0
        user = self.db.query(UserModel).filter(UserModel.id == uid).first()
        return int(user.daily_calorie_goal or 0) if user else 0

    def get_consumed_calories_for_day(self, current_user: dict | None, target_date: str) -> int:
        uid = _current_user_id(current_user)
        if not uid:
            return 0
        meals = self.db.query(MealModel).filter(
            MealModel.user_id == uid,
            MealModel.completion_date == target_date,
        ).all()
        return sum(m.calories or 0 for m in meals)

    def get_remaining_calories_for_day(self, current_user: dict | None, target_date: str) -> int:
        return self.get_daily_calorie_goal(current_user) - self.get_consumed_calories_for_day(current_user, target_date)

    def show_daily_calorie(self, current_user: dict | None, target_date: str) -> dict[str, int]:
        return {
            "daily_goal": self.get_daily_calorie_goal(current_user),
            "consumed_today": self.get_consumed_calories_for_day(current_user, target_date),
            "remaining_calories": self.get_remaining_calories_for_day(current_user, target_date),
        }


class MealTracker:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add_meal(
        self,
        current_user: dict | None,
        meal_name: str,
        meal_type: str,
        calorie_in_meal: int,
        completion_date: str,
        time_of_log: str | None = None,
        notes: str = "",
        protein: int = 0,
        carbs: int = 0,
        fats: int = 0,
    ) -> dict[str, Any]:
        uid = _current_user_id(current_user)
        if not uid:
            raise ValueError("Current user not found")
        record = MealModel(
            id=generate_id(),
            user_id=uid,
            meal_name=meal_name,
            meal_type=meal_type,
            calories=int(calorie_in_meal),
            protein=int(protein),
            carbs=int(carbs),
            fats=int(fats),
            completion_date=completion_date,
            time_of_log=time_of_log or now_dubai(),
            notes=notes,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        logger.info("Meal added successfully")
        return _meal_to_dict(record)

    def view_meal(self, current_user: dict | None) -> list[dict[str, Any]]:
        uid = _current_user_id(current_user)
        if not uid:
            return []
        records = self.db.query(MealModel).filter(MealModel.user_id == uid).all()
        return [_meal_to_dict(m) for m in records]

    def find_meal(self, current_user: dict | None, meal_id: str) -> dict[str, Any] | None:
        uid = _current_user_id(current_user)
        if not uid:
            return None
        record = self.db.query(MealModel).filter(
            MealModel.user_id == uid,
            MealModel.id == meal_id,
        ).first()
        return _meal_to_dict(record) if record else None

    def update_meal(
        self,
        current_user: dict | None,
        meal_id: str,
        updated_meal_name: str,
        updated_meal_type: str,
        updated_meal_in_calorie: int,
        updated_time_of_log: str,
        updated_completiton_date: str,
        updated_notes: str,
        updated_protein: int = 0,
        updated_carbs: int = 0,
        updated_fats: int = 0,
    ) -> dict[str, Any] | None:
        uid = _current_user_id(current_user)
        if not uid:
            return None
        record = self.db.query(MealModel).filter(
            MealModel.user_id == uid,
            MealModel.id == meal_id,
        ).first()
        if not record:
            return None
        record.meal_name = updated_meal_name
        record.meal_type = updated_meal_type
        record.calories = int(updated_meal_in_calorie)
        record.protein = int(updated_protein)
        record.carbs = int(updated_carbs)
        record.fats = int(updated_fats)
        record.time_of_log = updated_time_of_log
        record.completion_date = updated_completiton_date
        record.notes = updated_notes
        self.db.commit()
        logger.info("Meal updated successfully")
        return _meal_to_dict(record)

    def delete_meal(self, current_user: dict | None, meal_id: str) -> bool:
        uid = _current_user_id(current_user)
        if not uid:
            return False
        record = self.db.query(MealModel).filter(
            MealModel.user_id == uid,
            MealModel.id == meal_id,
        ).first()
        if not record:
            return False
        self.db.delete(record)
        self.db.commit()
        logger.info("Meal deleted successfully")
        return True


class MealPlanService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_meal_plan(
        self,
        current_user: dict | None,
        plan_name: str,
        goal: str,
        daily_target_calories: int,
        daily_target_protein: int,
        daily_target_carbs: int,
        daily_target_fats: int,
        meals: list[dict[str, Any]],
    ) -> dict[str, Any]:
        uid = _current_user_id(current_user)
        if not uid:
            raise ValueError("Current user not found")
        if not meals:
            raise ValueError("Meal plan must contain at least one meal slot")
        exists = self.db.query(MealPlanModel).filter(
            MealPlanModel.user_id == uid,
            MealPlanModel.plan_name.ilike(plan_name.strip()),
        ).first()
        if exists:
            raise ValueError("A meal plan with this name already exists")
        record = MealPlanModel(
            id=generate_id(),
            user_id=uid,
            plan_name=plan_name.strip(),
            goal=goal,
            daily_target_calories=int(daily_target_calories),
            daily_target_protein=int(daily_target_protein),
            daily_target_carbs=int(daily_target_carbs),
            daily_target_fats=int(daily_target_fats),
            meals=meals,
            created_at=now_dubai(),
            updated_at=now_dubai(),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return _meal_plan_to_dict(record)

    def list_meal_plans(self, current_user: dict | None) -> list[dict[str, Any]]:
        uid = _current_user_id(current_user)
        if not uid:
            return []
        records = self.db.query(MealPlanModel).filter(MealPlanModel.user_id == uid).all()
        return [_meal_plan_to_dict(p) for p in records]

    def get_meal_plan(self, current_user: dict | None, identifier: str) -> dict[str, Any] | None:
        uid = _current_user_id(current_user)
        if not uid:
            return None
        record = self.db.query(MealPlanModel).filter(
            MealPlanModel.user_id == uid,
            MealPlanModel.id == identifier,
        ).first()
        if not record:
            record = self.db.query(MealPlanModel).filter(
                MealPlanModel.user_id == uid,
                MealPlanModel.plan_name.ilike(identifier.strip()),
            ).first()
        return _meal_plan_to_dict(record) if record else None

    def start_meal_plan_day(self, current_user: dict | None, identifier: str) -> dict[str, Any]:
        plan = self.get_meal_plan(current_user, identifier)
        if not plan:
            raise ValueError("Meal plan not found")
        return plan


class NutritionSummaryService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def calculate_daily_nutrition_summary(
        self,
        current_user: dict | None,
        calculation_date: str,
    ) -> dict[str, Any] | None:
        if not validate_date_input(calculation_date):
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        uid = _current_user_id(current_user)
        if not uid:
            return None
        meals = self.db.query(MealModel).filter(
            MealModel.user_id == uid,
            MealModel.completion_date == calculation_date,
        ).all()
        if not meals:
            return None
        calorie_tracker = CalorieTracker(self.db)
        return {
            "date": calculation_date,
            "calories_consumed": sum(m.calories or 0 for m in meals),
            "protein_consumed": sum(m.protein or 0 for m in meals),
            "carbs_consumed": sum(m.carbs or 0 for m in meals),
            "fats_consumed": sum(m.fats or 0 for m in meals),
            "daily_calorie_goal": calorie_tracker.get_daily_calorie_goal(current_user),
            "remaining_calories": calorie_tracker.get_remaining_calories_for_day(current_user, calculation_date),
        }


class Workout_Repository:
    def __init__(self, db: Session):
        self.db = db

    def log_workout_entry(self, current_user: dict | None, sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        uid = _current_user_id(current_user)
        if not uid:
            return []
        saved = []
        for s in sessions:
            record = WorkoutSessionModel(
                id=s.get("id") or generate_id(),
                user_id=uid,
                name=s.get("name", ""),
                blocks=s.get("blocks", []),
                notes=s.get("notes", ""),
                created_at=s.get("created_at") or now_dubai(),
                updated_at=now_dubai(),
            )
            self.db.add(record)
            saved.append(s)
        self.db.commit()
        return saved

    def list_workout_entries(self, current_user: dict | None) -> list[dict[str, Any]]:
        uid = _current_user_id(current_user)
        if not uid:
            return []
        records = self.db.query(WorkoutSessionModel).filter(WorkoutSessionModel.user_id == uid).all()
        return [_workout_to_dict(w) for w in records]

    def list_worout_entries(self, current_user: dict | None) -> list[dict[str, Any]]:
        return self.list_workout_entries(current_user)

    def get_entry(self, current_user: dict | None, entry_id: str) -> dict[str, Any] | None:
        uid = _current_user_id(current_user)
        if not uid:
            return None
        record = self.db.query(WorkoutSessionModel).filter(
            WorkoutSessionModel.user_id == uid,
            WorkoutSessionModel.id == entry_id,
        ).first()
        return _workout_to_dict(record) if record else None


class WorkoutSessionService:
    def __init__(self, db: Session):
        self.db = db

    def create_session(
        self,
        user_id: str,
        name: str,
        workout_details: list[dict[str, Any]],
        notes: str,
    ) -> dict[str, Any]:
        session = {
            "id": generate_id(),
            "user_id": user_id,
            "name": name.strip(),
            "blocks": workout_details,
            "notes": notes,
            "created_at": now_dubai(),
            "updated_at": now_dubai(),
        }
        self.validate_session(session)
        return session

    def add_strength_exercise(self, label: str, name: str, exercises: list[dict[str, Any]]) -> dict[str, Any]:
        return {"block_type": "strength", "label": label, "name": name, "exercises": exercises}

    def add_cardio_exercise(self, label: str, minutes: int, intensity: str) -> dict[str, Any]:
        return {"block_type": "cardio", "label": label, "minutes": int(minutes), "intensity": intensity}

    def add_exercise(self, name: str, sets: list[dict[str, Any]]) -> dict[str, Any]:
        return {"name": name, "sets": sets}

    def validate_session(self, session: dict[str, Any]) -> None:
        if not session.get("name"):
            raise ValueError("Session name is required")
        if not session.get("blocks"):
            raise ValueError("Session must have at least one block")

    def log_session(
        self,
        current_user: dict | None,
        session_name: str,
        workout_blocks: list[dict[str, Any]],
        notes: str = "",
    ) -> dict[str, Any]:
        uid = _current_user_id(current_user)
        if not uid:
            raise ValueError("Current user not found")
        session = self.create_session(
            user_id=uid,
            name=session_name,
            workout_details=workout_blocks,
            notes=notes,
        )
        Workout_Repository(self.db).log_workout_entry(current_user, [session])
        return session


class RoutineService:
    def __init__(self, db: Session):
        self.db = db

    def create_routine(self, current_user: dict | None, name: str, days: list[dict[str, Any]]) -> dict[str, Any]:
        uid = _current_user_id(current_user)
        if not uid:
            raise ValueError("Current user not found")
        if not name.strip():
            raise ValueError("Routine name is required")
        if not days:
            raise ValueError("Routine must contain at least one day")
        record = RoutineModel(
            id=generate_id(),
            user_id=uid,
            name=name.strip(),
            days=days,
            created_at=now_dubai(),
            updated_at=now_dubai(),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return _routine_to_dict(record)

    @staticmethod
    def add_routine_day(day_name: str, blocks: list[dict[str, Any]]) -> dict[str, Any]:
        if not day_name.strip():
            raise ValueError("Day name is required")
        return {"day_name": day_name.strip(), "blocks": blocks}

    @staticmethod
    def format_routine(routine: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": routine.get("id"),
            "name": routine.get("name"),
            "day_count": len(routine.get("days", [])),
            "created_at": routine.get("created_at"),
            "updated_at": routine.get("updated_at"),
        }

    def list_routines(self, current_user: dict | None) -> list[dict[str, Any]]:
        uid = _current_user_id(current_user)
        if not uid:
            return []
        records = self.db.query(RoutineModel).filter(RoutineModel.user_id == uid).all()
        return [_routine_to_dict(r) for r in records]

    def get_routine(self, current_user: dict | None, identifier: str) -> dict[str, Any] | None:
        uid = _current_user_id(current_user)
        if not uid:
            return None
        record = self.db.query(RoutineModel).filter(
            RoutineModel.user_id == uid,
            RoutineModel.id == identifier,
        ).first()
        if not record:
            record = self.db.query(RoutineModel).filter(
                RoutineModel.user_id == uid,
                RoutineModel.name.ilike(identifier.strip()),
            ).first()
        return _routine_to_dict(record) if record else None

    def build_session_from_routine(
        self,
        current_user: dict | None,
        day_name: str,
        routine_name: str | None = None,
    ) -> dict[str, Any]:
        uid = _current_user_id(current_user)
        if not uid:
            raise ValueError("Current user not found")
        q = self.db.query(RoutineModel).filter(RoutineModel.user_id == uid)
        if routine_name:
            q = q.filter(RoutineModel.name.ilike(routine_name.strip()))
        routines = q.all()
        matching_routine = None
        matching_day = None
        for routine in routines:
            for day in (routine.days or []):
                if day.get("day_name", "").strip().lower() == day_name.strip().lower():
                    matching_routine = routine
                    matching_day = day
                    break
            if matching_day:
                break
        if not matching_routine or not matching_day:
            raise ValueError("Routine day not found")
        return WorkoutSessionService(self.db).log_session(
            current_user=current_user,
            session_name=f"{matching_routine.name} - {matching_day.get('day_name')}",
            workout_blocks=matching_day.get("blocks", []),
            notes=f"Built from routine: {matching_routine.name}",
        )
