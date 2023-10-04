import datetime
import csv
import logging
import pandas as pd
from prettytable import PrettyTable


logging.basicConfig(filename='todo_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Task:
    '''
    Represents a task with a description, due date, and completion status.
    '''
    def __init__(self, description, due_date=None, completed=False):
        '''
        Initializes a Task object with the given description, due date, and completion status.

        Args:
            description (str): Description of the task.
            due_date (date, optional): Due date of the task. Defaults to None.
            completed (bool, optional): Completion status of the task. Defaults to False.
        '''
        self.description = description
        self.due_date = due_date
        self.completed = completed
    
    def mark_as_completed(self):
        '''
        Marks the task as completed.
        '''
        self.completed = True
        logging.info(f"Task '{self.description}' marked as completed.")

    def mark_as_pending(self):
        '''
        Marks the task as pending (not completed).
        '''
        self.completed = False
        logging.info(f"Task '{self.description}' marked as pending.")

    def set_due_date(self, due_date):
        '''
        Sets the due date of the task.

        Args:
            due_date (date): Due date of the task.
        '''
        self.due_date = due_date
        logging.info(f"Due date of task '{self.description}' set to {self.due_date}.")

    def to_dict(self):
        '''
        Converts the task object to a dictionary for CSV storage.

        Returns:
            dict: Dictionary representation of the task.
        '''
        return {
            "description": self.description,
            "due_date": str(self.due_date),
            "completed": self.completed
        }
        
        
    def determine_due_status(self):
        """
        Determines the due status of the task based on its due date.

        Returns:
            str: Due status of the task.
        """
        today = pd.Timestamp.now().date()
        if self.due_date == today:
            return 'Due today'
        elif self.due_date > today:
            return 'On time'
        elif self.due_date < today:
            return 'Past due'
        
        
    def __str__(self):
        '''
        String representation of the task.

        Returns:
            str: Formatted task description with status and due date (if available).
        '''
        status = self.determine_due_status()
        status_str = f", {status}" if status else ""
        return f"{self.description} - {status}{status_str}"

class TaskManager:
    '''
    Manages tasks, including adding, marking as completed, marking as pending, deleting, viewing, saving, and loading tasks.
    '''
    def __init__(self):
        '''
        Initializes an empty TaskManager object.
        '''
        self.tasks = []

    def add_task(self, task):
        '''
        Adds a task to the task list.

        Args:
            task (Task): Task object to be added.
        '''
        self.tasks.append(task)
    
    def mark_task_as_completed(self, task_description):
        '''
        Marks a task as completed based on its description.

        Args:
            task_description (str): Description of the task to be marked as completed.
        '''
        for task in self.tasks:
            if task.description == task_description:
                task.mark_as_completed()
    
    def mark_task_as_pending(self, task_description):
        '''
        Marks a task as pending based on its description.

        Args:
            task_description (str): Description of the task to be marked as pending.
        '''
        for task in self.tasks:
            if task.description == task_description:
                task.mark_as_pending()
    
    def delete_task(self, task_description):
        '''
        Deletes a task based on its description.

        Args:
            task_description (str): Description of the task to be deleted.
        '''
        self.tasks = [task for task in self.tasks if task.description != task_description]
    
    def view_tasks(self, filter_type=None):
        '''
        Views tasks based on the filter type.

        Args:
            filter_type (str, optional): Filter type for viewing tasks (all/completed/pending). Defaults to None.

        Returns:
            list: List of tasks based on the filter type.
        '''
        if filter_type == "completed":
            filtered_tasks = [task for task in self.tasks if task.completed]
        elif filter_type == "pending":
            filtered_tasks = [task for task in self.tasks if not task.completed]
        else:
            filtered_tasks = self.tasks
        return filtered_tasks
    
    def save_to_csv(self, filename="tasks.csv"):
        '''
        Saves tasks to a CSV file in the format "description,due_date,completed,determine_due_status".

        Args:
            filename (str, optional): Name of the CSV file. Defaults to "tasks.csv".
        '''
        with open(filename, mode='w', newline='') as file:
            fieldnames = ["description", "due_date", "completed", "due_status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                task_dict = task.to_dict()
                task_dict["due_status"] = task.determine_due_status()
                writer.writerow(task_dict)


    def load_from_csv(self, filename="tasks.csv"):
        '''
        Loads tasks from a CSV file and returns a list of Task objects.

        Args:
            filename (str, optional): Name of the CSV file. Defaults to "tasks.csv".

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

            
def get_due_date_from_user():
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
    
def get_user_choice():
    '''
    Gets the user's choice from the menu.

    Returns:
        int: User's choice as an integer.
    '''
    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= 7:
            return int(choice)
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
           
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

def main():
    '''
    Main function to run the task management application.
    '''
    task_manager = TaskManager()
    task_manager.tasks = load_tasks_from_csv()
    
    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Mark Task as Completed")
        print("3. Mark Task as Pending")
        print("4. Delete Task")
        print("5. View Tasks")
        # print("6. Undo")
        print("6. Exit")
        
        choice = get_user_choice()

        if choice == 1:
            description = input("Enter task description: ")
            due_date = get_due_date_from_user()
            task = Task(description, due_date)
            task_manager.add_task(task)
            task_manager.save_to_csv() 
            print("Task added successfully!")

        elif choice == 2:
            task_description = input("Enter task description to mark as completed: ")
            task_manager.mark_task_as_completed(task_description)
            task_manager.save_to_csv()
            print("Task marked as completed.")
            logging.info(f"Task '{task_description}' marked as completed.")

        elif choice == 3:
            task_description = input("Enter task description to mark as pending: ")
            task_manager.mark_task_as_pending(task_description)
            task_manager.save_to_csv()
            print("Task marked as pending.")
            logging.info(f"Task '{task_description}' marked as pending.")

        elif choice == 4:
            task_description = input("Enter task description to delete: ")
            task_manager.delete_task(task_description)
            task_manager.save_to_csv()
            print("Task deleted successfully.")
            logging.info(f"Task '{task_description}' deleted.")


        elif choice == 5:
            filter_type = input("Enter filter type (all/completed/pending): ").lower()
            if filter_type == "all":
                tasks = task_manager.tasks
            elif filter_type == "completed":
                tasks = [task for task in task_manager.tasks if task.completed]
            elif filter_type == "pending":
                tasks = [task for task in task_manager.tasks if not task.completed]
            else:
                print("Invalid filter type. Showing all tasks.")
                tasks = task_manager.tasks

            table = PrettyTable(["Description", "Due Date", "Completed", "Due Status"])
            table.align["Description"] = "l"
            table.align["Due Date"] = "c"
            table.align["Completed"] = "c"
            table.align["Due Status"] = "c"

            for task in tasks:
                table.add_row([task.description, task.due_date, task.completed, task.determine_due_status()])

            print(table)


        # elif choice == 6:
        #     if caretaker.undo(task_manager):
        #         print("Undo successful!")
        #     else:
        #         print("Unable to undo.")
        
        elif choice == 6:
            print("Exiting...")
            task_manager.save_to_csv()
            break

if __name__ == "__main__":
    main()
