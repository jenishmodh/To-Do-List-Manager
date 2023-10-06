
import csv
from task import Task

import logging
logging.basicConfig(filename='todo_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import datetime

class InputHandler:
    def get_user_choice(self):
        '''
        Gets the user's choice from the menu.

        Returns:
            int: User's choice as an integer.
        '''
        while True:
            choice = input("Enter your choice: ")
            if choice.isdigit() and 1 <= int(choice) <= 8:
                return int(choice)
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")

    def get_due_date_from_user(self):
        '''
        Gets the due date from the user.

        Returns:
            date: Due date entered by the user.
        '''
        while True:
            due_date = input("Enter due date (YYYY-MM-DD, optional) or press Enter: ")
            if not due_date:
                return None
            try:
                due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
                return due_date
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                logging.error("Invalid date format entered by the user: %s", due_date)

    def load_tasks_from_csv():
        '''
        Loads tasks from a CSV file.

        Returns:
            list: List of Task objects loaded from the CSV file.
        '''
        tasks = []
        try:
            with open("tasks.csv", mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    due_date = datetime.datetime.strptime(row['due_date'], "%Y-%m-%d").date() if row['due_date'] else None
                    task = Task(row['description'], due_date, eval(row['completed']))
                    tasks.append(task)
            print("Tasks loaded successfully!")
        except FileNotFoundError:
            print("No tasks found.")
        return tasks
