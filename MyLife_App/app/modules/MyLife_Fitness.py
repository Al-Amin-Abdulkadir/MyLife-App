import json
from pathlib import Path

from app.modules.MyLife_Tracker import *

fitness_database = Path(__file__).resolve().parents[2] / "data" / "fitness.json"
def load_fitness_database():
    if not fitness_database.exists():
        return {
            "daily_claorie_goal" : 0,
            "meal_log" : [],
            "workout_sessions" : [],
            "routines": [],
            "meal_plans" : []
        }
    with open(fitness_database, "r") as fitness_file:
        return json.load(fitness_file) 

def save_fitness_database(fitness_data):
    with open(fitness_database, "w") as fitness_file:
        json.dump(fitness_data, fitness_file, indent=4)
class CalorieTracker:
    def __init__(self, data_saver=save_fitness_database, data_loader=load_fitness_database):
        self.load_fitness_data = data_loader
        self.save_fitness_data = data_saver
    
    def set_calorie_goal(self, goal : int):
        fitness_data = self.load_fitness_data()
        fitness_data["user_fitness_data"]["meal_system"]["daily_calorie"] = int(goal)
        self.save_fitness_data(fitness_data)

    def get_daily_calorie_goal(self) -> int:
        fitness_data = self.load_fitness_data()
        return int(fitness_data["user_fitness_data"]["meal_system"]["daily_calorie"])

    def get_consumed_calories_for_day(self, target_date : str) -> int:
        fitness_data = self.load_fitness_data()
        consumed_today = 0

        for meal in fitness_data.get("meal_log", []):
            if meal.get("completion_date") == target_date:
                consumed_today += int(meal.get("calories", 0))
        return consumed_today

    def get_remaining_calories_for_day(self, target_date: str) -> int:
        daily_goal = self.get_daily_calorie_goal()
        consumed_today = self.get_consumed_calories_for_day(target_date)
        return daily_goal - consumed_today

    def show_daily_calorie(self, target_date: str):
        print(f"Daily goal : {self.get_daily_calorie_goal()} cal")
        print(f"Consumed today : {self.get_consumed_calories_for_day(target_date)} cal")
        print(f"Remaining calories for today : {self.get_remaining_calories_for_day(target_date)} cal")
class MealTracker:
    def __init__(self,data_saver : save_fitness_database, data_loader : list[dict[str, Any]] = load_database) -> None:
        self.load_fitness_data = data_loader
        self.save_fitness_data = data_saver

    def add_meal(self,
                meal_name : str,
                meal_type : str,
                calorie_in_meal : int,
                completetion_date : str,
                time_of_log : now_dubai,
                notes : str
                ) -> dict[str, Any]:

                fitness_data = self.load_fitness_data()
                meal = {
                "id" : generate_id(),
                "meal" : meal_name,
                "meal type" : meal_type,
                "calories" : int(calorie_in_meal),
                "time_of_log" : now_dubai(),
                "completion_date" : completetion_date,
                "notes" : notes
                }
                fitness_data.setdefault("meal_log", []).append(meal)
                self.save_fitness_data(fitness_data)
                logging.INFO("Meal added successfully")
                return meal

    def update_meal(self,
                    updated_meal_name : str,
                    updated_meal_type : str,
                    updated_meal_in_calorie : int,
                    updated_time_of_log : str,
                    updated_completiton_date : now_dubai,
                    updataed_notes : str  ) -> dict[str, Any] | None:
                    fitness_data = self.load_fitness_data()
                    for meal in fitness_data.get("meal", []):
                        if meal.get("users", []):
                            meal.update({
                            "meal" : updated_meal_name,
                            "meal type" : updated_meal_type,
                            "calories" : updated_meal_in_calorie,
                            "time_of_log" : updated_time_of_log,
                            "completion_date" : updated_completiton_date,
                            "notes" : updataed_notes
                        })
                        logging.INFO("Meal updated successfully")
                        self.save_fitness_data(fitness_data)
                        return meal
                    return None

    def delete_meal(self, meal_id : str) -> bool:
         fitness_data = self.load_fitness_data()
         meal_log = fitness_data.get("meal_log", [])

         updated_meal_log = [meal for meal in meal_log if str(meal.get("id")) != str(meal_id)]

         if len(updated_meal_log) == len(meal_log):
              return False
         
         fitness_data["meal_log"] = updated_meal_log
         self.save_fitness_data(fitness_data)
         logging.INFO("Meal updated successfully")
         return True

    def view_meal(self):
        fitness_data = self.load_fitness_data()
        return [meal for meal in fitness_data.get("meal_log", []) if meal]


def _log_meal(current_user : ensure_current_user):
    if not current_user:
        print("Current user not found")
        return
    
    fitness_data = load_fitness_database()
    while True:
        meal_name = input("\nEnter meal name : ").strip().lower()
        if not meal_name:
            print("\nMeal name cannot be empty")
            continue
        if len(meal_name) < 2:
            print("\nMeal name cannot be less than two characters")
            continue
        break

    while True:
        meal_type = input("\nEnter meal type (breakfast/lunch/dinner/snack) : ").strip().lower()
        if not meal_type:
            print("Meal type cannot be empty")
            continue
        meal_type_registry : list[str] = [
            "breakfast",
            "lunch",
            "dinner",
            "snack"
            ]
        if meal_type not in meal_type_registry:
                print(f"\nMeal type should be one of the following {meal_type_registry}")
                continue
        break
        
    while True:
        calories = input("\nEnter calories for this meal : ").strip()
        if not calories:
            print("Calories cannot be empty")
            continue
        if not calories.isdigit():
            print("Calories must be a number")
            continue
        calories = int(calories)
        if calories <= 0:
            print("Calories must be above 0")
            continue
        break
        
    while True:
        completion_date = input("\nEnter a completion date (YYYY-MM-DD) or press enter for today : ").strip()
        if not completion_date:
            completion_date = now_dubai().split("T")[0]
        try:
            datetime.strptime(completion_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format")
            continue
        break

    notes = input("Enter notes (optional) : ").strip()

    meal = {
        "id" : generate_id(),
        "meal_name" : meal_name,
        "meal_type" : meal_type,
        "calories" : calories,
        "completion_date": completion_date,
        "time_of_log" : now_dubai(),
        "notes" : notes
    }
    fitness_data.setdefault("meal_log", []).append(meal)
    save_fitness_database(fitness_data)
    print("\nMeal logged successfully")
    logging.info(f"\nMeal logged successfully for {current_user}")
    print("\nMeal summary")
    calorie_tracker = CalorieTracker()
    print(f"\nMeal name : {meal_name}")
    print(f"\nCalories for meal : {calories}")
    print(f"\nDaily goal : {calorie_tracker.get_daily_calorie_goal()} calories")
    print(f"\nRemaining today : {calorie_tracker.get_remaining_calories_for_day(completion_date)} calories")
    print(f"\n consumed today : {calorie_tracker.get_consumed_calories_for_day(completion_date)} calories ")
        
def _view_meals(current_user : ensure_current_user) -> list[dict[str, Any]]:
    if not current_user:
        print("Current user not found")
        return
    fitness_data = load_fitness_database()
    meal_log = fitness_data.get("meal_log", [])
    if not meal_log:
        print("meal log not found")
        return []

    print("===Meal history===")
    for index, meal in enumerate(meal_log, start=1):
        print(
            f"{index}. {meal.get("id")} | {meal.get("meal")} |"
            f"{meal.get("meal type")} | {meal.get("calories")} |" 
            f"{meal.get("completion_date")}"
        )
    return meal_log 
    
def _view_meal_details(current_user : ensure_current_user):
    if not current_user:
        print("Current user not found")
        return
    fitness_data = load_fitness_database()
    
    meal_log = _view_meals(current_user)
    
    while True:
        meal_choice = input("Enter a meal name or number : ").strip()
        selected_meal = None

        if meal_choice.isdigit():
            meal_number = int(meal_choice)
            meal_index = meal_number - 1

            if 0 <= meal_index < len(meal_log):
                selected_meal = meal_log[meal_index]
        
        else:
            for meal in meal_log:
                if meal.get("meal", "").strip().lower() == meal_choice.lower():
                    selected_meal = meal

        if selected_meal:
            break

        print("meal not found. Please enter a valid meal name or 3-digit number.") 
    
    print("\n=== Meal Details ===")
    print(f"Meal ID: {selected_meal.get('id')}")
    print(f"Meal Name: {selected_meal.get('meal_name', selected_meal.get('meal'))}")
    print(f"Meal Type: {selected_meal.get('meal_type', selected_meal.get('meal type'))}")
    print(f"Calories: {selected_meal.get('calories')}")
    print(f"Completion Date: {selected_meal.get('completion_date')}")
    print(f"Time of Log: {selected_meal.get('time_of_log')}")
    print(f"Notes: {selected_meal.get('notes')}")

    return selected_meal

    
def create_meal_plan(current_user : ensure_current_user):
    if not current_user:
        print("Current user not found")
        return
    
    fitness_data = load_fitness_database()
    while True:
        meal_plan_name = input("\nEnter meal plan name : ").strip()
        if not meal_plan_name:
            print("Name required")
            continue

        if len(meal_plan_name) <= 2:
            print("Name has to be at least 3 characters")
            continue

        duplicate_found = False
        for plan in fitness_data.get("meal_plans", []):
            existing_name = plan.get("plan_name", plan.get("meal_plan_name", "")).strip().lower()
            if existing_name == meal_plan_name.lower():
                duplicate_found = True
                break

        if duplicate_found:
            print("A meal plan with this name already exists")
            continue
        break

    allowed_options: list[str] = [
        "fat loss",
        "maintenance",
        "muscle gain"
    ]
    while True:
        plan_goal = input("\nGoal (fat loss / maintenance / muscle gain) : ").strip().lower()
        if not plan_goal:
            print("Goal required")
            continue

        if plan_goal not in allowed_options:
            print(f"Plan goal should be one of the following {allowed_options}")
            continue
        break

    while True:
        daily_target_calories = input("\nDaily Target Calories : ").strip()
        if not daily_target_calories:
            print("Target calories required")
            continue

        if not daily_target_calories.isdigit():
            print("Calories must be a number")
            continue

        daily_target_calories = int(daily_target_calories)
        if daily_target_calories <= 0:
            print("Daily calories must be above zero")
            continue
        break

    while True:
        daily_target_proteins = input("\nDaily Target Proteins : ").strip()
        if not daily_target_proteins:
            print("Target proteins required")
            continue

        if not daily_target_proteins.isdigit():
            print("Target proteins must be a number")
            continue
        
        daily_target_proteins = int(daily_target_proteins)
        break

    while True:
        daily_target_carbs = input("\nDaily target carbs : ").strip()
        if not daily_target_carbs:
            print("Target carbs is required")
            continue

        if not daily_target_carbs.isdigit():
            print("Carbs must be a number")
            continue

        daily_target_carbs = int(daily_target_carbs)
        if daily_target_carbs <= 0:
            print("Daily carbs must be above zero")
            continue
        break

    while True:
        daily_target_fats = input("\nDaily target fats : ").strip()
        if not daily_target_fats:
            print("Target fats is required")
            continue

        if not daily_target_fats.isdigit():
            print("Target fats must be a number")
            continue

        daily_target_fats = int(daily_target_fats)
        if daily_target_fats <= 0:
            print("Daily fats must be above zero")
            continue
        break

    meals = []
    meal_type_registry = ["breakfast", "lunch", "dinner", "snack"]

    while True:
        while True:
            meal_type = input("\nEnter meal type for this slot (breakfast/lunch/dinner/snack) : ").strip().lower()
            if not meal_type:
                print("Meal type required")
                continue

            if meal_type not in meal_type_registry:
                print(f"Meal type must be one of the following: {meal_type_registry}")
                continue
            break

        foods = []
        while True:
            food_item = input("Enter food item for this meal slot (or type 'done') : ").strip()
            if not food_item:
                print("Food item cannot be empty")
                continue

            if food_item.lower() == "done":
                if not foods:
                    print("Add at least one food item before finishing this meal slot")
                    continue
                break

            foods.append(food_item)

        meal_notes = input("Enter notes for this meal slot (optional) : ").strip()
        meals.append({
            "meal_type": meal_type,
            "foods": foods,
            "notes": meal_notes
        })

        add_another_meal = input("\nAdd another meal slot? (y/n) : ").strip().lower()
        while add_another_meal not in ["y", "n"]:
            print("Enter 'y' or 'n'")
            add_another_meal = input("Add another meal slot? (y/n) : ").strip().lower()

        if add_another_meal == "n":
            break

    if not meals:
        print("Meal plan must contain at least one meal slot")
        return

    meal_plan = {
        "id": generate_id(),
        "entry_type": "meal_plan",
        "plan_name": meal_plan_name,
        "goal": plan_goal,
        "daily_target_calories": daily_target_calories,
        "daily_target_protein": daily_target_proteins,
        "daily_target_carbs": daily_target_carbs,
        "daily_target_fats": daily_target_fats,
        "meals": meals,
        "created_at": now_dubai(),
        "updated_at": now_dubai()
    }

    fitness_data.setdefault("meal_plans", []).append(meal_plan)
    save_fitness_database(fitness_data)

    print("\nMeal plan created successfully")
    print(f"Plan name: {meal_plan_name}")
    print(f"Goal: {plan_goal}")
    print(
        f"Targets: {daily_target_calories} cal | "
        f"{daily_target_proteins} protein | "
        f"{daily_target_carbs} carbs | "
        f"{daily_target_fats} fats"
    )
    print(f"Meal slots added: {len(meals)}")

def view_meal_plans(current_user : ensure_current_user) -> list[dict[str, Any]]:
    if not current_user:
        print("Current user not found")
        return
    
    fitness_data = load_fitness_database()
    meal_plan_log = fitness_data.get("meal_plans", [])
    if not meal_plan_log:
        print("You do not have any meal plan")
        return []
    
    print(f"===Meal plans===")

    for index, meal_plan in enumerate(meal_plan_log, start=1):
        print(
            f"\n{index}. {meal_plan.get('plan_name')} | {meal_plan.get('goal')} | "
            f"{meal_plan.get('daily_target_calories')} cal | "
            f"{meal_plan.get('daily_target_protein')} protein | "
            f"{meal_plan.get('daily_target_carbs')} carbs | "
            f"{meal_plan.get('daily_target_fats')} fats"
        )
        return meal_plan_log

def view_meal_plan_structure(current_user : ensure_current_user):
    if not current_user:
        print("Current user not found")
        return
    fitness_data = load_fitness_database()
    meal_plan_log = fitness_data.get("meal_plans", [])
    if not meal_plan_log:
        print("Meal plan log not found")
        return []
    
    while True:
        plan_choice = input("\nEnter a meal plan name or number").strip()
        if not plan_choice:
            print("\nEnter a name or number to view a meal plan")
            continue
        selected_plan = None

        if plan_choice.isdigit():
            plan_number = int(plan_choice)
            plan_index = plan_number - 1

            if 0 <= plan_index < len(meal_plan_log):
                selected_plan = meal_plan_log[plan_index]
        
        else:
            for plan in meal_plan_log:
                if plan.get("plan_name", "").strip().lower() == plan_choice.lower():
                    selected_plan = plan
        
        if selected_plan:
            break

        print("plan name not found. Please enter a valid plan name or number")
    
    print("\n===meal plan details===")
    print(f"Meal plan ID : {selected_plan.get('id')}")
    print(f"entry type : {selected_plan.get('entry_type')}")
    print(f"Meal plan name : {selected_plan.get('plan_name')}")
    print(f"Goal : {selected_plan.get('goal')}")
    print(f"Daily Target calories : {selected_plan.get('daily_target_calories')} calories")
    print(f"Daily Target Carbs : {selected_plan.get('daily_target_carbs')} carbs")
    print(f"Daily Target Proteins : {selected_plan.get('daily_target_protein')} proteins")
    print(f"Daily Target fats : {selected_plan.get('daily_target_fats')} fats")
    print(f"Created at : {selected_plan.get('created_at')}")
    meal_slots = selected_plan.get("meals", [])

    if not meal_slots:
        print("No meal slots found in this meal plan.")
        return selected_plan

    print("\n=== Meal Slots ===")
    for index, meal in enumerate(meal_slots, start=1):
        print(f"\n{index}. Meal Type: {meal.get('meal_type')}")
        print(f"Foods: {', '.join(meal.get('foods', []))}")
        print(f"Notes: {meal.get('notes')}")


    return selected_plan

    

def _start_meal_plan_day(current_user : ensure_current_user):
     if not current_user:
        print("Current user not found")
        return

def _prompt_food_items():
    pass

def _prompt_macros():
    pass

def _calculate_daily_nutrition_summary(current_user : ensure_current_user):
    if not current_user:
        return

class Workout_Repository:
    def __init__(self,
                data_saver : save_fitness_database, 
                data_loader : list[dict[str, Any]] = load_database):
                self.load_fitness_data = data_loader
                self.save_fitness_data = data_saver
    
    def log_workout_entry(self,
                        entry_list : list[dict[str, Any]]
                        ) -> list[dict[str, Any]]:

                        fitness_data = self.load_fitness_data()
                        fitness_data.setdefault("workout_sessions", [])
                        self.save_fitness_data()
                        return entry_list
         
    
    def list_worout_entries(self) -> dict | None:
        fitness_data = self.load_fitness_data()
        return fitness_data.setdefault("workout_sessions", [])
    
    def get_entry(self,
                entry_id : str
                ) -> dict | None:
        for entry in self.list_worout_entries():
            if str(entry.get("id")) == str(entry_id):
                return entry
        return None
    
class WorkoutSessionService:
    def create_session(self,
                    name : str,
                    workout_details : dict[str, Any],
                    notes : str
                    ) -> dict[str, Any]:
        session = {
            "id" : generate_id(),
            "entry_type": session,
            "name" : name,
            "blocks" : workout_details,
            "notes" : notes,
            "created_at" : now_dubai(),
            "updated_at" : now_dubai()
        }
        self.validate_session()
        return session

    def add_strength_exercise(current_user : dict,
                            label : str ,
                            name : str,
                            exercises : list[dict[str, Any]]
                            ) -> list[dict[str, Any]]:
        return {
            "block_type" : "strength",
            "label" : label,
            "name" : name,
            "exercises" : exercises
        }
    
    def add_cardio_exercise(current_user : dict,
                            label : str,
                            minutes : int ,
                            intensity : str 
                            ) -> dict:
        return {
            "block_type" : "cardio",
            "label" : label,
            "minutes" : int(minutes),
            "intensity" : intensity
        }
    
    def add_exercise(name : str, 
                    sets : list[dict[str, Any]]
                    )->list[dict]:
        return {
             "name" : name,
             "sets" : sets
        }
    
    def validate_session(session : dict) -> None:
        if not session.get("name"):
            raise ValueError("Session name is required")
        if not session.get("blocks"):
            raise ValueError("Session must have at leat one block")

    def format_session(session : str) -> str:
        pass

class RoutineService:
    def __init__(self,
                data_saver : save_fitness_database, 
                get_user : ensure_current_user, 
                data_loader : list[dict[str, Any]] = load_database):
                self.get_user = get_user
                self.load_fitness_data = data_loader
                self.save_fitness_data = data_saver
    
    def create_routine(self, name : str, days : list[dict]) -> dict:
        pass
    
    def add_routine_day(day_name : str, blocks : list[dict[str, Any]]) :
        pass
    def format_routine(self, routine : dict) -> dict:
        pass
    def build_session_from_routine(self, day_name : str) -> dict:
        pass

def _log_workout_session(current_user : ensure_current_user):
    if not current_user:
        return

def _create_routine(current_user : ensure_current_user):
    if not current_user:
        return

def _start_routine_day(current_user : ensure_current_user):
    if not current_user:
        return

def _view_sessions(current_user : ensure_current_user) -> dict[str, Any]:
    if not current_user:
        return

def _view_sessions_details(current_user : ensure_current_user) -> dict[str]:
    if not current_user:
        return
    
def _view_routines(current_user : ensure_current_user) -> list[dict[str, Any]]:
    if not current_user:
        return

def view_routine_structure(current_user : ensure_current_user):
     if not current_user:
        return
     
def _prompt_session_name():
    pass

def _prompt_workout_blocks():
    pass

def _prompt_strength_exercises():
    pass

def _prompt_cardio_block():
    pass

def _prompt_routine_name():
    pass

def _prompt_routine_days():
    pass

def _prompt_day_structure():
    pass

     

def FitnessOverviewDashboard(current_user : ensure_current_user,) -> None:
    if not current_user:
        return None
    while True:
        print("\nDashboard")
        


# Features to be implemented in MyFitness:
# 1. Edit and delete workout/body metric records.
# 2. Goal target tracking with deadlines.
# 3. Weekly/monthly charts and progress trends.
# 4. Smart reminders for missed workout days.
