#calendar tracker for MyLife app
from app.modules.MyLife_Tracker import *


def _get_user_record(current_user):
    data = load_database()
    user = next(
        (u for u in data.get("users", []) if str(u.get("id")) == str(current_user.get("id"))),
        None,
    )
    return data, user


def _add_event(current_user):
    data, user = _get_user_record(current_user)
    if not user:
        print("Current user not found.")
        return

    title = input("Event title: ").strip()
    event_type = input("Event type (e.g. work, personal, meeting): ").strip().lower()
    event_date = input("Event date (YYYY-MM-DD HH:MM): ").strip()
    notes = input("Event notes: ").strip()

    user.setdefault("calendar_events", []).append(
        {
            "id": generate_id(),
            "title": title or "untitled",
            "event_type": event_type or "general",
            "event_date": event_date,
            "notes": notes,
            "created_at": now_dubai(),
            "updated_at": now_dubai(),
        }
    )
    save_database(data)
    print("Event added to calendar.")


def _view_all_events(current_user):
    _, user = _get_user_record(current_user)
    if not user:
        print("Current user not found.")
        return

    events = user.get("calendar_events", [])
    if not events:
        print("No calendar events found.")
        return

    print("\n=== Calendar Events ===")
    for index, event in enumerate(events, start=1):
        print(
            f"{index}. {event.get('title', 'untitled')} - {event.get('event_date', '')} "
            f"[{event.get('event_type', 'general')}]"
        )
        if event.get("notes"):
            print(f"   notes: {event.get('notes')}")


def _group_events_by_type(current_user):
    _, user = _get_user_record(current_user)
    if not user:
        print("Current user not found.")
        return

    grouped = {}
    for event in user.get("calendar_events", []):
        event_type = str(event.get("event_type", "general")).lower()
        grouped[event_type] = grouped.get(event_type, 0) + 1

    if not grouped:
        print("No events to group.")
        return

    print("\n=== Events Grouped By Type ===")
    for event_type, total in grouped.items():
        print(f"- {event_type}: {total}")


def events_menu(current_user):
    while True:
        print("\n=== Events Menu ===")
        print("1. Add event")
        print("2. View all events")
        print("3. Group events by type")
        print("4. Back")
        user_request = input("Choose an option: ").strip()

        if user_request == "1":
            _add_event(current_user)
        elif user_request == "2":
            _view_all_events(current_user)
        elif user_request == "3":
            _group_events_by_type(current_user)
        elif user_request == "4":
            return
        else:
            print("Enter a valid option.")


def _show_upcoming_deadlines(current_user):
    _, user = _get_user_record(current_user)
    if not user:
        print("Current user not found.")
        return

    tasks = user.get("tasks", [])
    projects = user.get("projects", [])

    print("\n=== Upcoming Task Deadlines ===")
    found_task = False
    for task in tasks:
        deadline = task.get("task_deadline")
        if deadline:
            found_task = True
            print(f"- {task.get('task_name', 'untitled')}: {deadline}")
    if not found_task:
        print("No task deadlines found.")

    print("\n=== Upcoming Project Deadlines ===")
    found_project = False
    for project in projects:
        deadline = project.get("project_deadline")
        if deadline:
            found_project = True
            print(f"- {project.get('project_title', 'untitled')}: {deadline}")
    if not found_project:
        print("No project deadlines found.")


def deadlines_menu(current_user):
    while True:
        print("\n=== Deadlines Menu ===")
        print("1. View upcoming deadlines")
        print("2. Back")
        user_request = input("Choose an option: ").strip()

        if user_request == "1":
            _show_upcoming_deadlines(current_user)
        elif user_request == "2":
            return
        else:
            print("Enter a valid option.")


def reminders_menu(current_user):
    while True:
        print("\n=== Reminders Menu ===")
        print("1. View reminder placeholders")
        print("2. Back")
        user_request = input("Choose an option: ").strip()

        if user_request == "1":
            print("Reminder creation and notifications will be implemented in this menu.")
        elif user_request == "2":
            return
        else:
            print("Enter a valid option.")


def MyCalendar_dashboard(current_user):
    current_user = ensure_current_user(current_user)
    if not current_user:
        return False

    while True:
        _, user = _get_user_record(current_user)
        if not user:
            print("Current user not found.")
            return False

        print("\n=== MyCalendar Dashboard ===")
        print(f"Calendar events: {len(user.get('calendar_events', []))}")
        print(f"Tasks: {len(user.get('tasks', []))}")
        print(f"Projects: {len(user.get('projects', []))}")
        print("\n1. Events menu")
        print("2. Deadlines menu")
        print("3. Reminders menu")
        print("4. Back to main menu")
        user_request = input("Choose an option: ").strip()

        if user_request == "1":
            events_menu(current_user)
        elif user_request == "2":
            deadlines_menu(current_user)
        elif user_request == "3":
            reminders_menu(current_user)
        elif user_request == "4":
            app_dashboard(current_user)
            return True
        else:
            print("Enter a valid option.")


# Features to be implemented in MyCalendar:
# 1. Edit and delete events.
# 2. Date-based filtering and month view rendering.
# 3. Reminder scheduling with notification times.
# 4. External calendar sync support.
