from dataclasses import dataclass, field


@dataclass
class MealPlan:
    id: str
    plan_name: str
    goal: str
    daily_target_calories: int
    daily_target_protein: int
    daily_target_carbs: int
    daily_target_fats: int
    meals: list[dict] = field(default_factory=list)

