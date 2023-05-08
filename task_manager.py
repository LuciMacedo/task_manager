# =====importing libraries===========
import os
from datetime import date, datetime


def lines():
    print('=-' * 37)


DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    curr_t['id'] = task_components[6]

    task_list.append(curr_t)

# ====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print(f"{'=-' * 16}LOGIN{'=-' * 16}")
    curr_user = input("Username: ")
    lines()
    curr_pass = input("Password: ")
    lines()
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


def reg_user():
    """Add a new user to the user.txt file"""
    while True:
        # - Request input of a new username
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print('User name already exist. Try again!')
        else:
            break

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def add_task():
    """Allow a user to add a new task to task.txt file
                Prompt a user for the following:
                 - A username of the person whom the task is assigned to,
                 - A title of a task,
                 - A description of the task and
                 - the due date of the task."""
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # generate the id
    id_task = str(len(task_list) + 1)

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False,
        "id": id_task,
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No",
                t['id']
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def view_all():
    """Reads the task from task.txt file and prints to the console in the
               format of Output 2 presented in the task pdf (i.e. includes spacing
               and labelling)
            """

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']:^50}\n"
        disp_str += f"Assigned to: \t {t['username']:^40}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT):^46}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT):^55}\n"
        disp_str += f"Task Description:\n{t['description']}\n"
        disp_str += f"Id Task: \t {t['id']:^46}\n"
        print(disp_str)


def view_mine():
    """Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)"""
    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task: {t['title']:.>}\n"
            disp_str += f"Assigned to: {t['username']:^48}\n"
            disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT):^50}\n"
            disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT):^60}\n"
            disp_str += f"Task Description:\n{t['description']}\n"
            disp_str += f"Id Task: \t {t['id']}\n"
            disp_str += f"Task status:\t {'Yes' if t['completed'] else 'No'}"
            print(disp_str)
            lines()

        elif menu == 'ds' and curr_user == 'admin':
            '''If the user is an admin they can display statistics about number of users
                and tasks.'''
            num_users = len(username_password.keys())
            num_tasks = len(task_list)

            lines()
            print(f"Number of users: \t\t {num_users}")
            print(f"Number of tasks: \t\t {num_tasks}")
            lines()

    user_option_vm = int(input('''Select you option: 
            [1] Select a specific task by entering the ID number? 
            [2] Return to main menu? '''))
    if user_option_vm == 1:
        task_number = str(input('Enter your ID task number: '))
        for t in task_list:
            if (str(t['id'])) == task_number:
                user_edit_task = int(input('''Select one option
                    [1] Mark the task as completed.
                    [2] Edit the task.'''))
                if user_edit_task == 1:
                    t['completed'] = 'Yes'
                    print('Task completed! Well done :-)')
                elif user_edit_task == 2:
                    t['completed'] = 'No'
                    while True:
                        try:
                            new_due_date = input("New due date of task (YYYY-MM-DD): ")
                            new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                            t['due_date'] = new_due_date
                            print('Task date updated.')
                            break
                        except ValueError:
                            print("Invalid datetime format. Please use the format specified")
                elif t['completed'] == 'Yes':
                    print('Task already completed.')
    else:
        pass


def generate_report():

    # Calculate the number of completed, uncompleted and overdue tasks
    completed_tasks = len([tk for tk in task_list if tk['completed'] == True])
    uncompleted_tasks = len([tk for tk in task_list if tk['completed'] == False])
    overdue_tasks = len([tk for tk in task_list if tk['due_date'] < datetime.today() and
                         tk['completed'] == False])

    # Percentage for uncompleted and overdue tasks
    if len(task_list) > 0:
        uncompleted_percentage = round((uncompleted_tasks / len(task_list)) * 100, 2)
        overdue_percentage = round((overdue_tasks / len(task_list)) * 100, 2)
    else:
        uncompleted_percentage = 0
        overdue_percentage = 0

    with open('task_overview.txt', 'w+') as file:
        file.write('TASK OVERVIEW\n')
        file.write('=-' * 40)
        file.write(f"\nTotal number of tasks: {len(task_list)}\n")
        file.write('=-' * 40)
        file.write(f"\nTotal number of completed tasks: {completed_tasks}\n")
        file.write('=-' * 40)
        file.write(f"\nTotal number of uncompleted tasks: {uncompleted_tasks}\n")
        file.write('=-' * 40)
        file.write(f"\nTotal number of overdue tasks: {overdue_tasks}\n")
        file.write('=-' * 40)
        file.write(f"\nPercentage of uncompleted tasks: {uncompleted_percentage}%\n")
        file.write('=-' * 40)
        file.write(f"\nPercentage of overdue tasks: {overdue_percentage}%\n")
        file.write('=-' * 40)

        # Write report for the tasks to the file
        with open('user_overview.txt', 'w+') as file_user:
            file_user.write('\nUSER OVERVIEW\n')
            file_user.write('=-' * 40)
            file_user.write(f'\nTotal number of users: {len(username_password)}\n')
            file_user.write('=-' * 40)
            file_user.write(f'\nTotal number of tasks: {len(task_list)}\n')
            file_user.write('=-' * 40)

            # for loop to write in the user file
            for u in user_data:
                # display the username
                user_name = u.split(';')[0]
                file_user.write(f'\n{user_name}\n')
                file_user.write('=-' * 40)

                # Calculate the total tasks assign for that user
                num_assigned = len([tk for tk in task_list if tk['username'] == user_name])
                file_user.write(f"\nTotal number of tasks assigned: {num_assigned}\n")
                file_user.write('=-' * 40)

                # Percentage the total tasks assigned for every user
                percentage_task_user = round((num_assigned / len(task_list)) * 100, 2)
                file_user.write(f'\nPercentage tasks assigned: {percentage_task_user}\n')
                file_user.write('=-' * 40)

                # Calculate the total tasks completed
                num_completed = len([tk for tk in task_list if tk['completed'] == 'Yes'])
                file_user.write(f'''\nPercentage of the number of tasks assigned that have been completed: {num_completed}\n''')
                file_user.write('=-' * 40)

                # Calculate the total tasks still must be completed
                task_to_complete = len(
                    [tk for tk in task_list if tk['due_date'] > datetime.today() and tk['completed'] == 'No'])
                file_user.write(f'''\nPercentage of the number assigned to {user_name} that must still completed: {task_to_complete}\n''')
                file_user.write('=-' * 40)

                # Calculate the overdue tasks
                od_tasks = len(
                    [tk for tk in task_list if tk['due_date'] < datetime.today() and tk['completed'] == 'No'])
                # Calculate percentage of overdue tasks for every user
                if len(task_list) > 0:
                    o_percentage = round((od_tasks / len(task_list)) * 100, 2)
                else:
                    o_percentage = 0
                file_user.write(f'''\nPercentage of the number assigned to {user_name} that are overdue:
                {o_percentage}\n''')
                file_user.write('=-' * 40)


def display_statistics():
    if not os.path.exists("task_overview.txt" and "user_overview.txt"):
        generate_report()
    else:
        with open('task_overview.txt') as task_file, open('user_overview.txt') as user_file:
            task_statistics = task_file.readlines()
            for task_lines in task_statistics:
                t_lines = task_lines.strip()
                t_lines = t_lines.split(', ')
                print(t_lines[0])
            user_statistics = user_file.readlines()
            for user_lines in user_statistics:
                f_lines = user_lines.strip()
                f_lines = f_lines.split(', ')
                print(f_lines[0])


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
    [r] - Registering a user
    [a] - Adding a task
    [va] - View all tasks
    [vm] - View my task
    [gr] - Generate reports
    [ds] - Display statistics
    [e] - Exit
: ''').lower()
    lines()
    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        generate_report()
    elif menu == 'ds':
        display_statistics()
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice. Please Try again")
