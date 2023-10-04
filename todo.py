import datetime
import csv

class Task:
    def __init__(self, description, due_date=None, completed=False):
        self.description = description
        self.due_date = due_date
        self.completed = completed
    
    def mark_as_completed(self):
        self.completed = True
    
    def mark_as_pending(self):
        self.completed = False
    
    def set_due_date(self, due_date):
        self.due_date = due_date
    
    def to_dict(self):
        return {
            "description": self.description,
            "due_date": str(self.due_date),
            "completed": self.completed
        }
    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        due_date_str = f", Due: {self.due_date}" if self.due_date else ""
        return f"{self.description} - {status}{due_date_str}"

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
    
    def mark_task_as_completed(self, task_description):
        for task in self.tasks:
            if task.description == task_description:
                task.mark_as_completed()
    
    def mark_task_as_pending(self, task_description):
        for task in self.tasks:
            if task.description == task_description:
                task.mark_as_pending()
    
    def delete_task(self, task_description):
        self.tasks = [task for task in self.tasks if task.description != task_description]
    
    # def view_tasks(self, filter_type=None):
    #     if filter_type == "completed":
    #         return [task for task in self.tasks if task.completed]
    #     elif filter_type == "pending":
    #         return [task for task in self.tasks if not task.completed]
    #     else:
    #         return self.tasks
    def view_tasks(self, filter_type=None):
        if filter_type == "completed":
            filtered_tasks = [task for task in self.tasks if task.completed]
        elif filter_type == "pending":
            filtered_tasks = [task for task in self.tasks if not task.completed]
        else:
            filtered_tasks = self.tasks
        return filtered_tasks
    
    def save_to_csv(self, filename="tasks.csv"):
        with open(filename, mode='w', newline='') as file:
            fieldnames = ["description", "due_date", "completed"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow(task.to_dict())

    def load_from_csv(self, filename="tasks.csv"):
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    due_date = datetime.datetime.strptime(row['due_date'], "%Y-%m-%d").date() if row['due_date'] else None
                    task = Task(row['description'], due_date, eval(row['completed']))
                    self.add_task(task)
            print("Tasks loaded successfully!")
        except FileNotFoundError:
            print("No tasks found.")
            
def get_due_date_from_user():
    while True:
        due_date = input("Enter due date (YYYY-MM-DD, optional) or press Enter: ")
        if not due_date:
            return None
        try:
            due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
            return due_date
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

def get_user_choice():
    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= 7:
            return int(choice)
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
           
def load_tasks_from_csv():
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
    task_manager = TaskManager()
    task_manager.tasks = load_tasks_from_csv()   # Load tasks from CSV file at startup
    
    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Mark Task as Completed")
        print("3. Mark Task as Pending")
        print("4. Delete Task")
        print("5. View Tasks")
        print("6. Undo")
        print("7. Exit")
        
        choice = get_user_choice()

        if choice == 1:
            description = input("Enter task description: ")
            due_date = get_due_date_from_user()
            task = Task(description, due_date)
            task_manager.add_task(task)
            task_manager.save_to_csv()  # Save tasks to CSV after adding a task
            print("Task added successfully!")

        elif choice == 2:
            task_description = input("Enter task description to mark as completed: ")
            task_manager.mark_task_as_completed(task_description)
            task_manager.save_to_csv()  # Save tasks to CSV after marking as completed
            print("Task marked as completed!")

        elif choice == 3:
            task_description = input("Enter task description to mark as pending: ")
            task_manager.mark_task_as_pending(task_description)
            task_manager.save_to_csv()  # Save tasks to CSV after marking as pending
            print("Task marked as pending!")

        elif choice == 4:
            task_description = input("Enter task description to delete: ")
            task_manager.delete_task(task_description)
            task_manager.save_to_csv()  # Save tasks to CSV after deletion
            print("Task deleted successfully!")

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
            
            for task in tasks:
                print(task)

        elif choice == 6:
            print("Undo functionality not implemented.")
            # Implement undo functionality if required

        elif choice == 7:
            print("Exiting...")
            task_manager.save_to_csv()  # Save tasks to CSV file before exiting
            break

if __name__ == "__main__":
    main()
