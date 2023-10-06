import datetime
import csv

from task import Task

def save_to_csv(tasks:list, filename="tasks.csv"):
    '''
    Saves tasks to a CSV file in the format "description,due_date,completed,determine_due_status".
    Args:
        filename (str, optional): Name of the CSV file. Defaults to "tasks.csv".
    '''
    with open(filename, mode='w', newline='') as file:
        fieldnames = ["description", "due_date", "completed", "due_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            task_dict = task.to_dict()
            task_dict["due_status"] = task.determine_due_status()
            writer.writerow(task_dict)

def load_from_csv(filename="tasks.csv") -> list:
    '''
    Loads tasks from a CSV file and returns a list of Task objects
    Args:
        filename (str, optional): Name of the CSV file. Defaults to "tasks.csv"
    Returns:
        list: List of Task objects loaded from the CSV file.
    '''
    tasks = []
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                due_date = datetime.datetime.strptime(row['due_date'], "%Y-%m-%d").date() if row['due_date'] else None
                completed = eval(row['completed'])
                task = Task(row['description'], due_date, completed)
                tasks.append(task)
            print("Tasks loaded successfully!")
    except FileNotFoundError:
        print("No tasks found.")
    return tasks



