# Christian DeVore
# Main UI for To-Do/Task-management app (Sprint 1)

import datetime
import json
import random
import time

TASKS_DB = "task_list.json"

user_id = None      # By default the user is not logged in

#
# Prints the whitespace that "resets" the terminal (40 new lines of whitespace)
#
def printWhitespace():
    print("\n" * 40)


#
# Deletes a task from the system that has been marked as completed
#
def deleteTask():
    # Ask the user what task they would like to delete
    printWhitespace()
    print("Which task would you like to delete?")
    print("You may enter “B” to go back to the main screen.\n")
    task_to_delete = input("Enter your task here: ")
    if (task_to_delete == "B"):
        printWhitespace()
        return

    # Find the task in the database
    with open(TASKS_DB, "r+") as tasks: # open with read and write
        data = json.load(tasks) # converts into a python object
        for t in data["tasks"]:
            if t["name"] == task_to_delete:
                # Prompt the user if they are sure they want to delete this task
                inputting = True
                while (inputting):
                    print(f"\nAre you sure you want to delete “{task_to_delete}”? This action cannot be undone.") 
                    print("Type “Y” or “Yes” to proceed. Type “N” or “No” to cancel.\n")
                    confirm = str(input("Enter your choice here: "))
                    # User confirms, delete the task and update the file
                    if (confirm == "Yes" or confirm == "Y"):
                        data["tasks"].remove(t)
                        # Remove the existing contents of the database first, then insert all the old + new information
                        tasks.seek(0)
                        tasks.truncate()
                        json.dump(data, tasks, indent=4)
                        inputting = False

                        # Let the user know that the task has been deleted
                        printWhitespace()
                        print(f"Success! Your task {task_to_delete} has been deleted.\n")
                        return   

                    # User changes mind, make no changes
                    elif (confirm == "No" or confirm == "N"):
                        inputting = False
                        printWhitespace()
                        return
                    
                    # Wrong input entered
                    else:
                        printWhitespace()
                        print("Please enter \"Yes\"/\"Y\" or \"No\"/\"N\"")

        # The task does not exist in the database after checking through all tasks, inform the user this is the case
        printWhitespace()
        print(f"Error: \"{task_to_delete}\" was not found.\n")


# 
# Marks a task from the to-do list as complete and moves it into the "Completed" list
#
def completeTask():
    # Ask the user which task they have completed
    printWhitespace()
    print("Please enter which task you have completed.")
    print("You may enter “B” to go back to the main screen.\n")
    completed_task = input("Enter task name here: ")
    if (completed_task == "B"):
        printWhitespace()
        return

    # Find that task in the database
    with open(TASKS_DB, mode="r+") as tasks: # read and write (don't clear file)
        data = json.load(tasks) # converts into a python object
        
        # Go through the array of tasks in the database and check if the completed_task has a matching task
        for t in data["tasks"]:
            print(t["name"])
            if(t["name"] == completed_task):
                # Update the task's completion status if found
                t["completed"] = True;
                # Remove the existing contents of the database first, then insert all the old + new information
                tasks.seek(0)
                tasks.truncate()
                json.dump(data, tasks, indent=4)

                # Let the user know that the task has been marked as completed
                printWhitespace()
                print(f"Success! \"{completed_task}\" has been marked as completed.\n")
                return
        
        # Inform the user that their task does not exist if not found after searching through the whole database
        printWhitespace()
        print(f"Error: The specified task \"{completed_task}\" cannot be found.\n")


# 
# Creates a new task, which will be added
#
def createNewTask():
    # Inform the user they are creating a task and that they can backtrack
    printWhitespace()
    print("Provide the details for your new task below!")
    print("You may enter “B” any point go back to the main screen.\n")

    # Create new task object
    task_name = input("Enter the name of your new task: ")
    if (task_name == "B"):
        printWhitespace()
        return
    due_date = input("Enter the due date for this task: ")
    if (due_date == "B"):
        printWhitespace()
        return

    new_task = {
        "task_id": (int)(random.random() * 1000000),
        "name": task_name,
        "due_date": due_date,
        "completed": False
    }
        
    # Convert the database's data into a python object
    with open(TASKS_DB, mode="r+") as tasks: # read and write (don't clear file)
        data = json.load(tasks) # converts into a python object
        for t in data["tasks"]:
            if t["name"] == new_task["name"]:
                printWhitespace()
                print("\nError: Task already exists in the system!\n")
                return
        
        # Append the new task to the task list if it doesn't already exist
        data["tasks"].append(new_task)
        
        # Remove the existing contents of the database first, then insert all the old + new information
        tasks.seek(0)
        tasks.truncate()
        json.dump(data, tasks, indent=4)

        # Let the user know that the new task has been created
        printWhitespace()
        print(f"Success! Your new task \"{new_task["name"]}\" has been created!\n")


#
# Calls MICROSERVICE A to compare the order and content of two differnent lists
#    List #1: All tasks in the app
#    List #2: Custom list of the same length of the task list array that the user will input
#
def compareTaskLists():
    todo = []
    new_task_list = []

    # Check the database to get all names of tasks that are still TO-DO
    with open(TASKS_DB, "r") as tasks:
        data = json.load(tasks) # turns the JSON file into a python object called to
        for t in data["tasks"]:
            todo.append(t["name"]);

    # Append the names of the to-do tasks to the file
    print(f"Enter another set of {len(todo)} tasks below to compare their order and content similarity.")
    print("Enter \"B\" at any time to return to the main screen.")
    i = 1
    while (i < len(todo) + 1):
        t = input(f"Task {i}: ")
        if (t == "B"):
            printWhitespace()
            return
        new_task_list.append(t)
        i = i + 1

    # Place the todo list in the "prompt.txt" file in Microservice A folder
    path = "./MicroserviceA/prompt.txt"
    i = 1
    with open(path, "w") as file1:
        for t in todo:
            if (i != len(todo)):
                file1.write(t + ",")
            else:
                file1.write(t)
            i = i + 1

    # Place the new_task_list tasks in the "user_input.txt" file in Microservice A folder
    path = "./MicroserviceA/user_input.txt"
    i = 1
    with open(path, "w") as file2:
        for t in new_task_list:
            if (i != len(new_task_list)):
                file2.write(t + ",")
            else:
                file2.write(t)
            i = i + 1

    # Wait on the other microservice to process
    printWhitespace()
    print("Calculating simularity...")
    time.sleep(5)

    # Read the output from the microservice in the "compared_result.txt" file in Microservice A
    # folder and output this result to the user.
    path = "./MicroserviceA/compared_result.txt"
    with open(path, "r") as file3:
        result = file3.read()
        printWhitespace()
        print(f"{result} tasks were found in the same position.\n")



# 
# Print the details of a task, including:
#   - name
#   - due date
#
def printTaskDetails(t):
    print(t["name"])
    print("Due Date:", t["due_date"], "\n")


#
# Prints the tasks that the user still has in their to-do list and the tasks that have been completed
#
def printTasks():
    # Initialize arrays to store TO-DO and Completed tasks
    completed = []
    todo = []

    # Check the database to see what tasks are TO-DO and completed
    with open(TASKS_DB, "r") as tasks:
        data = json.load(tasks) # turns the JSON file into a python object called to
        for t in data["tasks"]:
            # Add the tasks status to the corresponding group (to-do array or completed array)
            if t["completed"] == True:
                completed.append(t)
            else:
                todo.append(t)

    # Print out all of the completed tasks
    print("To-Do:\n")
    for task in todo:
        printTaskDetails(task)
    print("\n")
    print("Completed:\n")
    for task in completed:
        printTaskDetails(task)
    print("\n")


# 
# Prints the help guide to help the user navigate around the program (IH #4 and #1)
#
def printHelp():
    printWhitespace()
    print("Help and Frequently Asked Questions (FAQ):\n")
    
    print("1. How do I navigate around the app?\n")

    print("  The app can be navigated around by typing in a number corresponding to a specific")
    print("  choice. You may always type “B” (except in the main menu) to go back to the menu.\n")

    print("2. What is the benefit of using the app?\n")

    print("  The app allows you to track which tasks in your life need to be completed and by")
    print("  when, allowing you to efficiently manage your time and stay up to date with work,")
    print("  school, or anything else important.\n")
  
    print("3. What does each option do?\n")

    print("   “Create a new task”: Creates a new task which will be added to your To-Do list. Your")
    print("   list will be empty without adding any tasks.\n")

    print("   “Mark a task as completed”: Allows you to designate that you have completed a")
    print("   task. This task will be moved to your “Completed” list from your To-Do list.\n")

    print("   “Delete a task”: Deletes a specified task from the system. This is helpful when completed")
    print("   tasks are no longer needed for reminders and so tasks will not be stuck in the system forever.\n")

    print("   “Help”: Brings you to the current menu for assistance with using the app.\n")

    print("   “Exit program”: Exits and closes out of the program.\n")

    # Keep prompting the user if they want to go back to the main screen
    while (True):
        i = input("Enter \"B\" to return to the main screen at any time: ")
        if i == "B":
            printWhitespace()
            break

#
# MICROSERVICE B:
# Handles the account/login manager by prompting the user for inputs, then passing this information to be 
# used by the account services microservice.
#
def handleLogin():
    COMM_PIPE = "./MicroserviceB/pipeB.txt"

    print("Welcome! Use this app to keep track of tasks that need to be completed to help you be productive!")
    print("Please enter one of the options to move forward.")
    print("\nNote: Accounts are used to store and keep track of your tasks so you can access them at a later date!")
    print("If this is your first time using this app, please select option #1: \"Create a new account\"")

    while(True):
        print("\nOptions:")
        print("1. Create a new account")
        print("2. Login to an existing account")

        choice = input("\nEnter your input here: ")
        
        # Create a new account
        if choice == "1":
            printWhitespace()
            print("Enter your new account details below. Enter \"B\" at any time to go back.")
            username = input("New Username: ")
            if username == "B":
                printWhitespace()
                continue
            password = input("Password: ")
            if password == "B":
                printWhitespace()
                continue
            # Confirm the user wants this as their password - have them re-enter it again
            if (password != input("Please confirm your password (re-enter password): ")):
                printWhitespace()
                print("Error: Passwords do not match.")
            else:
                # Passwords match (proceed)
                with open(COMM_PIPE, "r+") as acctmanager:
                    message = "create " + username + " " + password
                    acctmanager.write(message)
                time.sleep(1)

                with open(COMM_PIPE, "r+") as acctmanager:
                    # The result passed back will be the user's id to get their task information 
                    # (-1 indicates an incorrect username or password -> re-prompt user to ask for id)
                    acctmanager.seek(0)
                    user_id = acctmanager.read()
                    print("Id is " + user_id)
                    if (user_id == "0"):
                        printWhitespace()
                        print("Error: This username already is in use.")
                        continue
                    else:
                        # Continue with the main program now
                        break

        # Login
        elif choice == "2":
            printWhitespace()
            print("Enter your login information below. Enter \"B\" at any time to go back.")

            # Get username and passowrd (go back if the user enters "B")
            username = input("Username: ")
            if username == "B":
                printWhitespace()
                continue
            password = input("Password: ")
            if password == "B":
                printWhitespace()
                continue

            # Pass this username and password off to the account manager (microservice B)
            with open(COMM_PIPE, "r+") as acctmanager:
                message = "login " + username + " " + password
                acctmanager.write(message)
            time.sleep(1)
            with open(COMM_PIPE, "r+") as acctmanager:
                # The result passed back will be the user's id to get their task information 
                # (0 indicates an incorrect username or password -> re-prompt user to ask for id)
                acctmanager.seek(0)
                user_id = acctmanager.read()
                if (user_id == "0"):
                    printWhitespace()
                    print("Error: This username or password is incorrect.")
                    continue
                else:
                    # Continue with the main program now
                    break

        else:
            print("Error: You must enter a 1 or 2.")


#
# Prints the user's options on the main screen.
#
def printUserOptions():
    print("What would you like to do?")
    print("1. Create a new task")
    print("2. Mark a task as completed")
    print("3. Delete a task")
    print("4. Check task list similarity")
    print("5. Help")
    print("6. Exit program")

# 
# Where the program starts off at, and will continue until the user chooses to exit.
#
def main():
    # Prompt the user to login after lauching the program
    printWhitespace()
    handleLogin()

    # Print tasks in the to-do list, completed tasks, and finally the user's options for navigating the UI.
    printWhitespace()
    print("Logged in successfully!\n")
    while(True):
        printTasks()
        
        # Print out the user's options
        printUserOptions()
        
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

        elif (choice == "4"):
            compareTaskLists()

        elif (choice == "5"):
            printHelp()

        # Quit the program
        elif (choice == "6"):
            break;

        # Incorrect input
        else:
            printWhitespace()
            print("You must enter a number 1-5!\n")


# Run the main function to start off the program
main()