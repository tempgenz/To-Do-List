import csv
import sys

import tabulate


# the main function greets with a welcome message and info about how to use the program
# after informing about available action commands it calls the action function
def main():
    print("Welcome To Task Manager\n"
          "<commands>\n"
          "View:- enter 'view' to view your tasks\n"
          "Add:- enter 'add' to add a task\n"
          "Remove:- enter 'remove' to remove a task\n"
          "Mark:- enter 'mark' to mark your tasks as complete or pending or vise versa\n"
          "EXIT:- enter 'exit' to exit the program")
    action()


# the action function this one is called everytime the user completes any action to ask for next command
# this one just takes an input of what action user wants to perform and then calls the responsible function accordingly
# the input edge cases has been taken care of with necessary error messages and info
# this same function has exit command available if user wants to exit the program
def action():
    print("\n<EXIT>,<ADD>,<MARK>,<REMOVE>,<VIEW>\n")
    action_list = ["view", "add", "remove", "mark", "exit"]
    while True:
        actor = input("What do you wanna do ?\n: ").strip()
        if actor.lower() not in action_list:
            print("Enter a valid command it has to be <view,add,remove,mark or EXIT>")
            continue
        else:
            break
    if actor.lower() == action_list[0]:
        view_task()
    elif actor.lower() == action_list[1]:
        add_task()
    elif actor.lower() == action_list[2]:
        remove_task()
    elif actor.lower() == action_list[3]:
        mark_task()
    else:
        sys.exit("Thanks for using our program 👋🏻")


# the function to view recorded tasks a csv file which is being used to store users task data is opened
# csv reader reads the csv file and then the same data is stored in temp list
# then the temp list is used to print the tasks data in grid format using tabulate lib
# the action function is called after the printing to take next command
def view_task():
    if count() == 1:
        print("TASK LIST IS EMPTY\nif you wanna add tasks enter 'add'")
        action()
    else: pass
    csv_list = []
    with open("tasks.csv") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            csv_list.append(row)
    print(tabulate.tabulate(csv_list, headers="firstrow", tablefmt="grid"))
    action()


# the add function to add tasks in data structure which is csv file
# task is asked to user via input prompt and then saved in csv file using csv_dict_writer
# the task is saved as pending by default coz obviously why would someone enter a completed task
# the view task function is called after adding so user can see updated list
# and then the view function calls action to get next command
def add_task():
    task = input("Enter task: ").rstrip()
    with open("tasks.csv", 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['C', 'task', 'status'])
        writer.writerow({"C": count(), "task": task, "status": "pending"})
        print("TASK ADDED 👍🏻")
    view_task()


# this count function is used to count the length of rows in csv file which is then used to index tasks accordingly
# this function is called multiple times by other functions thus specified
def count():
    _ = []
    with open("tasks.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            _.append(row)
        return len(_)


# remove funtion to remove tasks from the list/csv_file
# first takes the input of user asking for the task number user wants to be removed and edge cases also handled
# read further into
def remove_task():
    if count() == 1:
        print("TASK LIST IS ALREADY EMPTY\nif you wanna add tasks enter 'add'")
        action()
    else: pass
    print("Enter the task number you want to remove\n"
          "the number is mentioned just before the task")
    while True:
        num = input("Enter the task number: ")
        if num.isdigit() and count() < int(num) or int(num) == 0:
            print(f"there is no task on number {num} place enter a valid count")
            continue
        elif num.isalpha():
            print("You have to enter a number please enter a valid task count")
            continue
        else:
            break
    # after valid input is given csv file is opened and temp list used to save data to manipulate
    # the row containing task that has to be removed is identified with valid input and not being saved in list
    with open("tasks.csv") as csv1:
        reader = csv.DictReader(csv1)
        _ = []
        place = 0
        for row in reader:
            if num != row['C']:
                place += 1
                row['C'] = place
                _.append(row)
            else:
                continue
    # the csv filed is opened again to overwrite using csv_dict_writer
    # data saved in the list saved to the csv file and this time without the task user want removed
    # view function is called after to see updated list
    with open("tasks.csv", 'w') as csv2:
        writer = csv.DictWriter(csv2, fieldnames=["C", "tasks", "status"])
        writer.writeheader()
        for row in _:
            writer.writerow({"C": row['C'], "tasks": row['tasks'], "status": row['status']})
    print("\nREMOVED 👍🏻")
    if count() == 1:
        print("TASK LIST IS EMPTY\nif you wanna add tasks enter 'add'")
        action()
    else: pass
    view_task()


# the mark function to change the status of task from pending to complete or vise versa
# first input is taken for task number and preferred status and edge cases being handled at the same time
# read further
def mark_task():
    if count() == 1:
        print("TASK LIST IS EMPTY\nif you wanna add tasks enter 'add'")
        action()
    else:
        pass
    while True:
        num = input("Which Task do you wanna mark?\nEnter the task number: ")
        if num.isdigit() and count() > int(num) != 0:
            break
        else:
            print("Please give a valid input Enter the task number you want to mark\n"
                  "the number is mentioned just before the task")
            continue
    while True:
        mark = input("What do you wanna change it to ?\npending or completed\n: ")
        if mark.lower() in ["pending", "complete", "completed"]:
            break
        else:
            print("invalid input please enter a valid command which could be\n'pending' or 'completed'")
    # csv file opened and data saved to temp list using csv_dict_reader after manipulated as desired
    with open("tasks.csv") as csv1:
        reader = csv.DictReader(csv1)
        dic = []
        for row in reader:
            if num == row['C']:
                if mark.lower() == row['status']:
                    print(f"Task number {num} is already {mark}")
                    action()
                row['status'] = 'completed'
                dic.append(row)
            else:
                dic.append(row)
                continue
    # csv file opened to overwrite the changed data saved in list using csv_dict_writer, view_task is called at end
    with open("tasks.csv", 'w') as csv2:
        writer = csv.DictWriter(csv2, fieldnames=["C", "tasks", "status"])
        writer.writeheader()
        for row in dic:
            writer.writerow({"C": row['C'], "tasks": row['tasks'], "status": row['status']})
    print("\nSTATUS CHANGED 👍🏻")
    view_task()


if __name__ == '__main__':
    main()
