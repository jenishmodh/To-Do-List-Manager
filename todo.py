import logging
from prettytable import PrettyTable
from task import Task, TaskManager
import utils
from users_csv import InputHandler

logging.basicConfig(filename='todo_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    task_manager = TaskManager()
    input_handler = InputHandler()
    task_manager.tasks = utils.load_from_csv()
    
    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Mark Task as Completed")
        print("3. Mark Task as Pending")
        print("4. Delete Task")
        print("5. View Tasks")
        print("6. Extend Deadline")
        print("7. Exit")
        
        choice = input_handler.get_user_choice()
        
        if choice == 1:
            description = input("Enter task description: ")
            due_date = input_handler.get_due_date_from_user()
            task = Task(description, due_date)
            task_manager.add_task(task)
            utils.save_to_csv(task_manager.tasks)
            print("Task added successfully!")

        elif choice == 2:
            task_description = input("Enter task description to mark as completed: ")
            task_manager.mark_task_as_completed(task_description)
            utils.save_to_csv(task_manager.tasks)
            print("Task marked as completed.")
            logging.info(f"Task '{task_description}' marked as completed.")

        elif choice == 3:
            task_description = input("Enter task description to mark as pending: ")
            task_manager.mark_task_as_pending(task_description)
            utils.save_to_csv(task_manager.tasks)
            print("Task marked as pending.")
            logging.info(f"Task '{task_description}' marked as pending.")

        elif choice == 4:
            task_description = input("Enter task description to delete: ")
            task_manager.delete_task(task_description)
            utils.save_to_csv(task_manager.tasks)
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

            def sort_key(task):
                if task.determine_due_status() == "Past due":
                    return 0
                elif task.determine_due_status() == "Due today":
                    return 1
                else:
                    return 2

            sorted_tasks = sorted(tasks, key=sort_key)

            table = PrettyTable(["Description", "Due Date", "Completed", "Due Status"])
            table.align["Description"] = "l"
            table.align["Due Date"] = "c"
            table.align["Completed"] = "c"
            table.align["Due Status"] = "c"

            for task in sorted_tasks:
                table.add_row([task.description, task.due_date, task.completed, task.determine_due_status()])

            print(table)


        elif choice == 6:
            task_description = input("Enter task description to modify the due date: ")
            for task in task_manager.tasks:
                if task.description == task_description:
                    new_due_date = input_handler.get_due_date_from_user()
                    task.set_due_date(new_due_date)
                    utils.save_to_csv(task_manager.tasks)
                    print(f"Due date of task '{task_description}' modified successfully.")
                    logging.info(f"Due date of task '{task_description}' modified to {new_due_date}.")
                    break
            else:
                print(f"Task with description '{task_description}' not found.")
                logging.error(f"Task with description '{task_description}' not found.")
                
        elif choice == 7:
            print("Exiting...")
            utils.save_to_csv(task_manager.tasks)
            break

if __name__ == "__main__":
    main()
