from app.modules.MyLife_Tracker import *

def _get_user_record(current_user):
    current_user = ensure_current_user()
    if not current_user:
        return
    
    data_loader = load_database()
    current_id = str(current_user)
    user = next((u for u in data_loader.get("users", []) if str(user.get("id")) == current_id), None)
    if not user:
        print("User not found")
        return False   


def MyStatistics_dashboard(current_user):
    current_user = ensure_current_user(current_user)
    if not current_user:
        return False

    while True:
        user = _get_user_record(current_user)
        if not user:
            print("Current user not found.")
            return False

        print("\n=== MyStatistics Dashboard ===")
        print(f"Tasks tracked: {len(user.get('tasks', []))}")
        print(f"Habits tracked: {len(user.get('habits', []))}")
        print(f"Projects tracked: {len(user.get('projects', []))}")
        print(f"Fitness logs: {len(user.get('fitness', []))}")
        print(f"Finance entries: {len(user.get('finance', []))}")
        print("\n1. Productivity analytics menu")
        print("2. Habit analytics menu")
        print("3. Finance analytics menu")
        print("4. Back to main menu")
        user_request = input("Choose an option: ").strip()

        if user_request == "1":
            pass
        elif user_request == "2":
            pass
        elif user_request == "3":
            pass
        elif user_request == "4":
            app_dashboard(current_user)
            return True
        else:
            print("Enter a valid option.")


# Features to be implemented in MyStatistics:
# 1. Time-range filtering (daily, weekly, monthly, custom).
# 2. Chart rendering for trend visualization.
# 3. Export analytics summaries.
# 4. Goal-vs-actual performance dashboards.
