from datetime import datetime
from argparse import ArgumentParser
from tabulate import tabulate
import json
import sys

"""
    Plan (super rough):
    1. Create a way to open json and save json
    2. Create functions for add, update, deleting tasks
    3. Create functions for marking as in progress or done
"""

def main() -> None:
    supported_queries = get_supported_queries()
    querie, args = get_querie(supported_queries)
    DATABASE_PATH = "task.json"
    database = load_database(DATABASE_PATH)
    # manipulate here
    try:
        querie(database, **args)
    except KeyError:
        sys.exit("No task found with provided ID")
    save_database(database, DATABASE_PATH)

def load_database(path: str) -> dict[str, dict]:
    """
        Loads the database as json file from specified path, creates if not found.
    """
    try:
        with open(path) as f:
            database = json.load(f)
    except FileNotFoundError:
        database = {}

    return database

def save_database(database: dict[str, dict], path: str) -> None:
    """
        Saves the database after use into the path.    
    """

    with open(path, "w") as f:
        json.dump(database, f)

def get_supported_queries() -> dict[str, dict]:
    """
        Returns a dictionary of keyword value pairs to be used to create an Argument Parser
    """
    return {
        "add": {
            "target": add_task,
            "help": "Add a new task to task list",
            "args": [
                {"name_or_flags": ["description"], "help": "Description of task"}
            ],
        },
        "update": {
            "target": update_task,
            "help": "Update an existing task",
            "args": [
                {"name_or_flags": ["id"], "help": "ID of existing task to update"},
                {"name_or_flags": ["description"], "help": "New description to update"}
            ],
        },
        "delete": {
            "target": delete_task,
            "help": "Delete a task",
            "args": [
                {"name_or_flags": ["id"], "help": "ID of task to delete"}
            ],
        },
        "mark-in-progress": {
            "target": mark_in_progress,
            "help": "Mark a task to be in progress",
            "args": [
                {"name_or_flags": ["id"], "help": "ID of task to mark in progress"}
            ],
        },
        "mark-done": {
            "target": mark_done,
            "help": "Mark a task to be done",
            "args": [
                {"name_or_flags": ["id"], "help": "ID of task to mark done"}
            ],
        },
        "list": {
            "target": list_tasks,
            "help": "List tasks in a table",
            "args": [
                {
                    "name_or_flags": ["status"], 
                    "help": "Status of tasks to filter by",
                    "choices": ["all", "todo", "in-progress", "done", ""],
                    "default": "all",
                    "nargs": "?",
                }
            ],
        },
    }

def get_querie(supported_queries: dict[str, dict]) -> tuple[callable, dict]:
    """
        Builds the argument parser, parses/validates the command line input, returning the appropriate function and arguments
    """
    parser = ArgumentParser(description="CLI Task Tracker from roadmap.sh")
    sub_parsers = parser.add_subparsers(dest="command", required=True)

    for name, properties in supported_queries.items():
        sub_parser = sub_parsers.add_parser(name, help=properties["help"])
        for arg in properties["args"]:
            sub_parser.add_argument(*arg.pop("name_or_flags"), **arg)

    args = parser.parse_args().__dict__
    querie = supported_queries[args.pop("command")]["target"]

    return querie, args    

def add_task(database: dict[str, dict], description: str) -> None:
    """
        Adds a new task, automatically assigning an ID
    """
    id = str(int(max("0", *database.keys())) + 1)
    today = datetime.now().isoformat()
    database[id] = {
        "description": description,
        "status": "todo",
        "createdAt": today,
        "updatedAt": today
    }
    print(f"Task added successfully (ID: {id})")
    list_tasks({id: database[id]})

def update_task(database: dict[str, dict], id: str, description: str) -> None:
    """
        Updates the description of an existing task
    """
    database[id]["description"] = description
    database[id]["updatedAt"] = datetime.now().isoformat()
    print(f"Task updated successfully (ID: {id})")
    list_tasks({id: database[id]})

def delete_task(database: dict[str, dict], id: str) -> None:
    """
        Deletes an existing task
    """
    del database[id]
    print(f"Task deleted successfully (ID: {id})")

def mark_in_progress(database: dict[str, dict], id: str) -> None:
    """
        Sets the status of a task to be 'in progress'
    """
    database[id]["status"] = "in-progress"
    database[id]["updatedAt"] = datetime.now().isoformat()
    print(f"Task marked as in-progress (ID: {id})")
    list_tasks({id: database[id]})

def mark_done(database: dict[str, dict], id: str) -> None:
    """
        Sets the status of atask to be 'done'
    """
    database[id]["status"] = "done"
    database[id]["updatedAt"] = datetime.now().isoformat()
    print(f"Task marked as done (ID: {id})")
    list_tasks({id: database[id]})

def list_tasks(database: dict[str, dict], status: str = "all") -> None:
    """
        List tasks based on status - default is 'all'
    """
    DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
    table = (
        {
            "ID": id,
            "Description": props["description"],
            "Status": props["status"],
            "Created At": datetime.fromisoformat(props["createdAt"]).strftime(DATETIME_FORMAT),
            "Updated At": datetime.fromisoformat(props["updatedAt"]).strftime(DATETIME_FORMAT),
        }
        for id, props in database.items()
        if status == "all" or status == props["status"]
    )
    
    print(tabulate(table, headers="keys", tablefmt="rounded_outline") or "Nothing to display")

if __name__ == '__main__':
    main()