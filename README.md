# Task Tracker CLI

A simple command-line task tracker built in Python. This tool allows you to add, delete, update, and manage tasks efficiently.

## Features
- Add new tasks
- Delete tasks
- Update task descriptions
- Mark tasks as "In Progress" or "Done"
- List tasks with optional filtering by status
- Persistent task storage using JSON

## Installation
### Prerequisites
Ensure you have Python installed (>=3.10 recommended).

### Clone the Repository
```sh
git clone <repository-url>
cd task-tracker-cli
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Usage
Run the script using:
```sh
python task_tracker.py <command> [arguments]
```

### Available Commands
- `add "description"` - Adds a new task.
- `delete <task_id>` - Deletes a task.
- `update <task_id> "new description"` - Updates a task's description.
- `mark-in-progress <task_id>` - Marks a task as "In Progress".
- `mark-done <task_id>` - Marks a task as "Done".
- `list [--status <status>]` - Lists tasks, optionally filtered by status.

## Example Usage
```sh
python task_tracker.py add "Finish project report"
python task_tracker.py list
python task_tracker.py mark-done 1
python task_tracker.py delete 2
```

## Data Persistence
Tasks are stored in `data.json`. Ensure this file is writable for proper functionality.

## License
This project is licensed under the MIT License.


