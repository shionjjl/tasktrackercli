from datetime import datetime
from argparse import ArgumentParser
import json
import sys



"""
    Plan (super rough):
    1. Create a way to open json and save json
    2. Create functions for add, update, deleting tasks
"""

def main():
    # TODO
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

def get_supported_queries():
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
    }

def get_querie(supported_queries: dict[str, dict]):
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
    id = str(int(max("0", *database.keys())) + 1)
    today = datetime.now().isoformat()
    database[id] = {
        "description": description,
        "status": "todo",
        "createdAt": today,
        "updatedAt": today
    }

def update_task(database: dict[str, dict], id: str, description: str) -> None:
    
    database[id]["description"] = description
    database[id]["updatedAt"] = datetime.now().isoformat()

def delete_task(database: dict[str, dict], id: str):
    del database[id]



if __name__ == '__main__':
    main()