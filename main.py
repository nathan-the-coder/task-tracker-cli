import argparse
import enum
import datetime
import json
import prettytable

tasks = []


class TaskStatus(enum.Enum):
    Todo = "Todo"
    InProgress = "InProgress"
    Done = "Done"


class Task:
    _id = 0

    def __init__(
        self, description: str, id=None, status=None, createdAt=None, updatedAt=None
    ) -> None:
        if id is None:
            Task._id += 1
            self.id = Task._id
        else:
            self.id = id
            Task._id = max(Task._id, id)

        self.description = description
        self.status = status or TaskStatus.Todo.name  # Store as string
        self.createdAt = createdAt or datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.updatedAt = updatedAt or None


def loadFromFile():
    global tasks
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            tasks = [Task(**task) for task in data]

            # Ensure the ID counter continues from the highest existing ID
            if tasks:
                Task._id = max(task.id for task in tasks)

    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []


def writeToFile():
    with open("data.json", "w") as file:
        json.dump([task.__dict__ for task in tasks], file, indent=4)


def add_task(description):
    tasks.append(Task(description))
    writeToFile()


def delete_task(task_id):
    global tasks
    task_id = int(task_id)
    tasks = [task for task in tasks if task.id != task_id]
    writeToFile()


def update_tasks(task_id, callback):
    for task in tasks:
        if task.id == task_id:
            callback(task)
            task.updatedAt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writeToFile()
            return True  # Indicate success
    return False  # Indicate failure


def update_task(task_id, new_description):
    task_id = int(task_id)
    loadFromFile()

    def update_description(task: Task):
        task.description = new_description

    if update_tasks(task_id, update_description):
        print(f"Task {task_id} updated successfully")
    else:
        print("Task not found")


def mark_task(new_status, task_id):
    task_id = int(task_id)
    loadFromFile()

    def update_status(task: Task):
        task.status = new_status.name  # Store as string

    if update_tasks(task_id, update_status):
        print(f"Task {task_id} marked as {new_status.name}")
    else:
        print("Task not found")


def list_tasks(query_status: str | None):
    global tasks
    loadFromFile()

    task_table = prettytable.PrettyTable()
    task_table.field_names = ["ID", "Description", "Status", "CreatedAt", "UpdatedAt"]

    for task in tasks:
        if query_status is not None:
            if task.status.lower() == query_status.lower():  # Fix comparison
                task_table.add_row([
                    task.id,
                    task.description,
                    task.status,
                    task.createdAt,
                    task.updatedAt,
                ])
        else:
            task_table.add_row([
                task.id,
                task.description,
                task.status,
                task.createdAt,
                task.updatedAt,
            ])

    print(task_table)


def main():
    loadFromFile()
    parser = argparse.ArgumentParser(
        description="Simple CLI app with multiple commands"
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", help="Task description")

    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", help="ID of the task to delete")

    # Update command
    parser_update = subparsers.add_parser("update", help="Update a task")
    parser_update.add_argument("id", help="ID of the task to update")
    parser_update.add_argument("new_description", help="New task description")

    # Mark InProgress and Mark Done command
    parser_mark_inprogress = subparsers.add_parser(
        "mark-in-progress", help="Mark a task as in-progress."
    )
    parser_mark_inprogress.add_argument(
        "id", help="ID of the task to mark as in-progress."
    )

    parser_mark_done = subparsers.add_parser(
        "mark-done", help="Mark a task as done or finished."
    )
    parser_mark_done.add_argument(
        "id", help="ID of the task to mark as done or finished."
    )

    # List command
    parser_list = subparsers.add_parser(
        "list", help="List all tasks based on the status queried or all the tasks"
    )
    parser_list.add_argument(
        "--status", help="Optional status to query", required=False
    )

    args = parser.parse_args()

    # Dispatch to the correct function
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

