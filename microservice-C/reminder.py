# Christian DeVore
# Reminders microservice (Microservice D) for To-do/Task-management app

import json
import time
from datetime import date

PIPE = "./pipeD.txt"

#
# The main program that handles creating and returning reminders for users
#
def main():
    while(True):
        try:
            with open(PIPE, "r+") as tasks:
                data = json.load(tasks)
                # Check if there are any uncompleted tasks due today, add to response if this is the case
                response = ""
                today = time.strptime(str(date.today()),"%Y-%m-%d")
                for t in data["tasks"]:
                    task_date = time.strptime((t["due_date"]), "%m/%d/%y")
                    if t["completed"] == False and task_date == today:
                        response = response + t["name"] + "\n"
                tasks.seek(0)
                tasks.truncate()
                if response == "":
                    tasks.write("0")    # 0 indicates no reminders needed
                else:
                    tasks.write("The following tasks are due today:\n" + response)
        except TypeError:
            pass
        except json.JSONDecodeError:
            pass
            



# Run the main program to start
main()