import logging
logging.basicConfig(filename='todo_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import pandas as pd

class TaskManager:
    '''
    Manages tasks, including adding, marking as completed, marking as pending, deleting, viewing, saving, and loading tasks.
    '''
    def __init__(self):
        '''
        Initializes an empty TaskManager object.
        '''
        self.tasks = []
        self.caretaker = Caretaker()

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
    

    def undo(self):
        '''
        Undo the last action performed by restoring the previous state.
        
        Returns:
            bool: True if undo was successful, False otherwise.
    '''
        if len(self.caretaker.mementos) > 1:
            memento = self.caretaker.get_memento(-2)
            self.tasks[-1].restore_from_memento(memento)
            self.caretaker.add_memento(memento)
            return True
        return False

    def redo(self):
        '''
    Redo the last undone action by restoring the next state.
    
    Returns:
        bool: True if redo was successful, False otherwise.
    '''
        if len(self.caretaker.mementos) > 1:
            memento = self.caretaker.get_memento(1)
            self.tasks[-1].restore_from_memento(memento)
            self.caretaker.add_memento(memento)
            return True
        return False


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
        
        
    def create_memento(self):
            return TaskMemento(self.description, self.due_date, self.completed)

    def restore_from_memento(self, memento):
        self.description = memento.description
        self.due_date = memento.due_date
        self.completed = memento.completed
        
        
        
    def __str__(self):
        '''
        String representation of the task.

        Returns:
            str: Formatted task description with status and due date (if available).
        '''
        status = self.determine_due_status()
        status_str = f", {status}" if status else ""
        return f"{self.description} - {status}{status_str}"

class TaskMemento:
    def __init__(self, description, due_date, completed):
        self.description = description
        self.due_date = due_date
        self.completed = completed
        

class Caretaker:
    def __init__(self):
        self.mementos = []

    def add_memento(self, memento):
        self.mementos.append(memento)

    def get_memento(self, index):
        return self.mementos[index]

