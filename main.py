import argparse
import enum
import datetime
import json

tasks = []

class TaskStatus(enum.Enum):
    Todo = enum.auto()
    InProgress = enum.auto()
    Done = enum.auto()

class Task:
    _id = 0
    def __init__(self, description: str, id=None, status=None, createdAt=None, updatedAt=None) -> None:
        if id is None:
            Task._id += 1
            self.id = Task._id
        else:
            self.id = id
            Task._id = max(Task._id, id)

        self.description = description
        self.status = status or TaskStatus.Todo.__str__()
        self.createdAt = createdAt or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updatedAt = updatedAt or None

def loadFromFile():
    global tasks
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            tasks = [Task(**task) for task in data]

            # Ensure the ID counter continues from the highest existing ID
            if tasks:
                Task._id = max(task.id for task in tasks)

    except (FileNotFoundError, json.JSONDecodeError):
        tasks = [] 


def writeToFile():
    with open('data.json', 'w+') as file:
        file.write(json.dumps([task.__dict__ for task in tasks], indent=4))

def add_task(description):
    tasks.append(Task(description))
    writeToFile()

def delete_task(task_id):
    global tasks
    task_id = int(task_id)

    # Find the task by ID
    tasks = [task for task in tasks if task.id != task_id]
    writeToFile()

def update_task(task_id, new_description):
    task_id = int(task_id)
    loadFromFile()

    for task in tasks:
        if task.id == task_id:
            task.description = new_description
            task.updatedAt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writeToFile()
            return

    print("Task not found")



def main():
    loadFromFile()
    parser = argparse.ArgumentParser(description="Simple CLI app with multiple commands")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", help="Task description")

    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", help="ID of the task to delete")

    # Update command
    parser_update = subparsers.add_parser("update", help="Update a task")
    parser_update.add_argument("id", help="ID of the task to update")
    parser_update.add_argument("new_description", help="new task description")

    args = parser.parse_args()

    # Dispatch to the correct function
    if args.command == "add":
        add_task(args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "update":
        update_task(args.id, args.new_description)

if __name__ == "__main__":
    main()

