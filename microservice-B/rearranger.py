# Christian DeVore
# Due date task re-arranger microservice (Microservice C) for To-do/Task-management app

import json
import time
from datetime import date

PIPE = "./pipeC.txt"

#
# The main program that handles creating and returning reminders for users
#
def main():
    while(True):
        try:
            with open(PIPE, "r+") as tasks:
                data = json.load(tasks)

                # Basic bubble sort algorithm in order to sort and print out tasks, sorted by the earliest due date
                num_tasks = len(data["tasks"])
                for i in range(num_tasks):
                    swapped_tasks = False
                    for j in range(i, num_tasks - i - 1):
                        date1 = time.strptime(data["tasks"][j]["due_date"], "%m/%d/%y")
                        date2 = time.strptime(data["tasks"][j + 1]["due_date"], "%m/%d/%y")
                        if date1 > date2:
                            # Swap tasks in the tasks array
                            temp = data["tasks"][j]
                            data["tasks"][j] = data["tasks"][j + 1]
                            data["tasks"][j + 1] = temp
                            swapped_tasks = True
                    # The array must be sorted if we have looked through the rest of it (starting at this index) and no swaps have been needed
                    if swapped_tasks == False:
                        break
                
                # Go through the newly sorted tasks list and create the output to send back to the user
                response = ""
                print(data["tasks"])
                for t in data["tasks"]:
                    response = response + t["name"] + "\nDue Date: " + t["due_date"] + "\n\n"
                tasks.seek(0)
                tasks.truncate()
                if response == "":
                    tasks.write("0")    # 0 indicates no reminders needed
                else:
                    tasks.write("Here is the sorted list of tasks, from earliest to latest due date:\n\n" + response)
        except json.JSONDecodeError:
            pass
        except TypeError:
            pass

            



# Run the main program to start
main()