from pydantic import BaseModel


class MealPlanSchema(BaseModel):
    plan_name: str
    goal: str
    daily_target_calories: int
    daily_target_protein: int
    daily_target_carbs: int
    daily_target_fats: int

