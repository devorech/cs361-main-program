# Christian DeVore
# Main UI for To-Do/Task-management app (Sprint 1)

import datetime
import json
import random

TASKS_DB = "task_list.json"

#
# Deletes a task from the system that has been marked as completed
#
def deleteTask():
    print("delete")


# 
# Marks a task from the to-do list as complete and moves it into the "Completed" list
#
def completeTask():
    # Ask the user which task they have completed
    print("\nWhich task have you completed?")
    completed_task = input("Enter task name here: ")

    # Find that task in the database
    tasks = open(TASKS_DB, mode="r+") # read and write (don't clear file)
    data = json.load(tasks) # converts into a python object
    
    # Go through the array of tasks in the database and check if the completed_task has a matching task
    isFound = False
    for t in data["tasks"]:
        print(t["name"])
        if(t["name"] == completed_task):
            # Update the task's completion status if found
            isFound = True;
            t["completed"] = True;
    
    # Inform the user that their task does not exist if not found after searching through the whole database
    if isFound == False:
        print(f"\nError: The specified task \"{completed_task}\" cannot be found.")

    # Close the tasks database file stream
    tasks.close()
    print("\n" * 40)

# 
# Creates a new task, which will be added
#
def createNewTask():
    # Create new task object
    new_task = {
        "task_id": (int)(random.random() * 1000000),
        "name": input("Enter the name of your new task: "),
        "due_date": input("Enter the due date for this task: "),
        "completed": False
    }
        
    # Convert the database's data into a python object
    tasks = open(TASKS_DB, mode="r+") # read and write (don't clear file)
    data = json.load(tasks) # converts into a python object
    data["tasks"].append(new_task)
    
    # Remove the existing contents of the database first, then insert all the old + new information
    tasks.seek(0)
    tasks.truncate()
    json.dump(data, tasks, indent=4)
    
    # Close the tasks database file stream
    tasks.close()
    print("\n" * 40)

#
# Prints the tasks that the user still has in their to-do list and the tasks that have been completed
#
def printTasks():
    tasks = open(TASKS_DB, "r")
    data = json.load(tasks) # turns the JSON file into a python object called to
    for t in data["tasks"]:
        print(t["name"])
        print("Due Date:", t["due_date"])

    tasks.close()

# 
# Where the program starts off at, and will continue until the user chooses to exit.
#
def main():
    while(True):
        # Print the welcome message, tasks in the to-do list, completed tasks, and finally the user's options
        # for navigating the UI.
        print("Welcome! Keep track of tasks that need to be completed to help you be productive!\n")
        printTasks()
        
        # Print out the user's options
        print("What would you like to do?")
        print("1. Create a new task")
        print("2. Mark a task as completed")
        print("3. Delete a completed task")
        print("4. Exit program")
        
        # Prompt user for input
        choice = input("Enter your input here: ")

        # User wants to create a new task to-do
        if (choice == "1"):
            createNewTask()

        # User wants to mark a task as completed
        elif (choice == "2"):
            completeTask()

        # User wants to delete a task that has been marked as completed.
        elif (choice == "3"):
            deleteTask()

        # Quit the program
        elif (choice == "4"):
            break;

        # Incorrect input
        else:
            print("You must enter a number 1-3!")

# Run the main function to start off the program
main()