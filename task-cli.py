import argparse
import enum
import datetime
import json
import prettytable

# List to store tasks
tasks = []

# Enum for task status
class TaskStatus(enum.Enum):
    Todo = "Todo"
    InProgress = "InProgress"
    Done = "Done"

# Task class to define a task object
class Task:
    _id = 0  # Class-level ID counter

    def __init__(
        self, description: str, id=None, status=None, createdAt=None, updatedAt=None
    ) -> None:
        if id is None:
            Task._id += 1
            self.id = Task._id
        else:
            self.id = id
            Task._id = max(Task._id, id)  # Ensure the ID counter remains correct

        self.description = description
        self.status = status or TaskStatus.Todo.name  # Store status as a string
        self.createdAt = createdAt or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updatedAt = updatedAt or None

# Load tasks from JSON file
def loadFromFile():
    global tasks
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            tasks = [Task(**task) for task in data]
            
            # Ensure ID counter continues correctly
            if tasks:
                Task._id = max(task.id for task in tasks)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

# Save tasks to JSON file
def writeToFile():
    with open("data.json", "w") as file:
        json.dump([task.__dict__ for task in tasks], file, indent=4)

# Add a new task
def add_task(description):
    tasks.append(Task(description))
    writeToFile()

# Delete a task by ID
def delete_task(task_id):
    global tasks
    task_id = int(task_id)
    tasks = [task for task in tasks if task.id != task_id]
    writeToFile()

# Generic function to update a task
def update_tasks(task_id, callback):
    for task in tasks:
        if task.id == task_id:
            callback(task)
            task.updatedAt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writeToFile()
            return True  # Return success
    return False  # Return failure

# Update task description
def update_task(task_id, new_description):
    task_id = int(task_id)
    loadFromFile()

    def update_description(task: Task):
        task.description = new_description

    if update_tasks(task_id, update_description):
        print(f"Task {task_id} updated successfully")
    else:
        print("Task not found")

# Update task status
def mark_task(new_status, task_id):
    task_id = int(task_id)
    loadFromFile()

    def update_status(task: Task):
        task.status = new_status.name  # Store as string

    if update_tasks(task_id, update_status):
        print(f"Task {task_id} marked as {new_status.name}")
    else:
        print("Task not found")

# List tasks with optional status filter
def list_tasks(query_status: str | None):
    global tasks
    loadFromFile()

    task_table = prettytable.PrettyTable()
    task_table.field_names = ["ID", "Description", "Status", "CreatedAt", "UpdatedAt"]

    for task in tasks:
        if query_status is not None:
            if task.status.lower() == query_status.lower():
                task_table.add_row([
                    task.id, task.description, task.status, task.createdAt, task.updatedAt
                ])
        else:
            task_table.add_row([
                task.id, task.description, task.status, task.createdAt, task.updatedAt
            ])

    print(task_table)

# Main function to parse and execute CLI commands
def main():
    loadFromFile()
    parser = argparse.ArgumentParser(
        description="Simple CLI app with multiple commands"
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # Add task command
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", help="Task description")

    # Delete task command
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", help="ID of the task to delete")

    # Update task description command
    parser_update = subparsers.add_parser("update", help="Update a task")
    parser_update.add_argument("id", help="ID of the task to update")
    parser_update.add_argument("new_description", help="New task description")

    # Mark task as in-progress command
    parser_mark_inprogress = subparsers.add_parser("mark-in-progress", help="Mark a task as in-progress.")
    parser_mark_inprogress.add_argument("id", help="ID of the task to mark as in-progress.")

    # Mark task as done command
    parser_mark_done = subparsers.add_parser("mark-done", help="Mark a task as done or finished.")
    parser_mark_done.add_argument("id", help="ID of the task to mark as done or finished.")

    # List tasks command
    parser_list = subparsers.add_parser("list", help="List all tasks based on the status queried or all the tasks")
    parser_list.add_argument("--status", help="Optional status to query", required=False)

    args = parser.parse_args()

    # Dispatch commands
    match args.command:
        case "add":
            add_task(args.description)
        case "update":
            update_task(args.id, args.new_description)
        case "delete":
            delete_task(args.id)
        case "mark-in-progress":
            mark_task(TaskStatus.InProgress, args.id)
        case "mark-done":
            mark_task(TaskStatus.Done, args.id)
        case "list":
            list_tasks(args.status)
        case _:
            raise Exception("Unknown command provided")

if __name__ == "__main__":
    main()

