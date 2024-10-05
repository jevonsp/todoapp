# funcs.py

import csv
from pathlib import Path
from typing import Tuple
from classes import User
import sys

def confirm() -> str:
    """Prompt user for confirmation and return 'y' or 'n'."""
    while True:
        user_input = input("Would you like to confirm? (Y/n): ").strip().lower()
        if user_input in ['y', 'n']:
            return user_input
        print("Invalid input. Please enter Y or N.")

def read_config(config_path: Path) -> dict:
    """Read configuration from file and return as dictionary."""
    variables = {}
    if config_path.exists():
        with config_path.open('r') as file:
            for line in file:
                key, value = line.strip().split(" = ")
                variables[key] = value.strip("'")
    return variables

def write_config(config_path: Path, name: str, tasks: int) -> None:
    """Write configuration to file."""
    with config_path.open('w') as file:
        file.write(f"name = '{name}'\n")
        file.write(f"tasks = {tasks}\n")

def get_user_info(user: User) -> Tuple[str, int]:
    """Get user information from config file or user input."""
    config_path = Path("config.txt")
    variables = read_config(config_path)

    if variables:
        user.name = variables.get('name', "")
        user.tasks = int(variables.get('tasks', 0))
    else:
        print("This is your first time using the program, enter your name")
        while not user.name:
            temp_name = input("Please enter your name: ")
            print(f"Is your name '{temp_name}'?")
            if confirm() == 'y':
                user.name = temp_name
                user.tasks = 0
                write_config(config_path, user.name, user.tasks)
                print(f"Thank you, {user.name}! You can proceed.")

    return user.name, user.tasks

def welcome(user: User) -> None:
    """Display welcome message."""
    print(f"Welcome, {user.name}, to PyPlanner. You have {user.tasks} tasks stored.")

def menu_logic(user: User) -> None:
    """Handle main menu logic."""
    menu_options = {
        '1': lambda: write_todo(user),
        '2': lambda: read_todo(user, 2),
        '3': lambda: read_todo(user, 3),
        '4': lambda: read_todo(user, 4),
        '5': lambda: sys.exit(0)
    }

    print("What would you like to do?")
    while True:
        menu_choice = input("1: Write Todo 2: Short 3: Med 4: Long 5: Exit -- ")
        action = menu_options.get(menu_choice)
        if action:
            action()
        else:
            print("Please input a valid response.\n1: Write Todo 2: Short 3: Med 4: Long 5: Exit  -- ")

def write_todo(user: User) -> None:
    """Write a new todo item."""
    csv_path = Path('todo.csv')

    if not csv_path.exists():
        with csv_path.open('w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Description', 'Time Frame'])

    while True:
        title = input("Enter the title: ")
        desc = input("Enter the description: ")
        period = get_valid_period()

        print("Are you happy with the following entry?")
        print(f"---\nTitle: {title}\nDescription: {desc}\nPeriod: {period}\n---")
        
        if confirm() == 'y':
            append_todo(csv_path, title, desc, period)
            user.incr_task()
            print(f"Todo added successfully! You have {user.tasks} tasks stored")
            break
        else:
            print("Please redo your entry.")

def get_valid_period() -> str:
    """Get a valid time frame input from the user."""
    while True:
        period = input("Enter the time frame (s: short-term, m: medium-term, l: long-term): ").strip().lower()
        if period in ['s', 'm', 'l']:
            return period
        print("Invalid entry. Please enter S, M, or L.")

def append_todo(csv_path: Path, title: str, desc: str, period: str) -> None:
    """Append a new todo item to the CSV file."""
    with csv_path.open('a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([title, desc, period])

def read_todo(user: User, menu_choice: int) -> None:
    """Read and display todo items based on time frame."""
    menu_choice_string = {2: "s", 3: "m", 4: "l"}
    time_frame = menu_choice_string.get(menu_choice)
    
    if time_frame is None:
        print("Invalid menu choice.")
        return
    
    csv_path = Path('todo.csv')
    if not csv_path.exists():
        print("No todo entries found. The todo.csv file does not exist.")
        return

    found = display_todos(csv_path, time_frame)
    temp_input = input("Would you like to modify the list? Y/n ").strip().lower()
    if temp_input == 'y':
        alter_list(user)
    else:
        menu_logic(user)

    if not found:
        print(f"No To-dos found.")
        print("Would you like to make one?")
        if confirm() == 'y':
            write_todo(user)
        else:
            menu_logic(user)

def display_todos(csv_path: Path, time_frame: str) -> bool:
    """Display todos for a specific time frame."""
    print(f"Reading {time_frame} To-dos:\n")
    found = False
    count = 1
    with csv_path.open('r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) == 3 and row[2].strip().lower() == time_frame:
                print(f"{count}. Title: {row[0]}\nDescription: {row[1]}\nTime Frame: {row[2]}\n")
                found = True
                count += 1
    return found

def alter_list(user: User) -> None:
    """Code for altering the todo list."""
    csv_path = Path('todo.csv')
    while True:
        if not csv_path.exists():
            print("The todo.csv file does not exist.")
            return

        # Display the current todos to the user
        print("Current To-Do List:")
        found = display_todos(csv_path, 's') or display_todos(csv_path, 'm') or display_todos(csv_path, 'l')

        if not found:
            print("No todo items available to modify.")
            return

        # Ask the user which entry they want to delete
        entry_number = input("Enter the number of the entry you wish to delete (or type 'cancel' to go back): ").strip()

        if entry_number.lower() == 'cancel':
            print("Operation cancelled.")
            return

        # Validate input to ensure it's a number
        try:
            entry_number = int(entry_number)
        except ValueError:
            print("Invalid input. Please enter a valid entry number.")
            return

        # Now, read the todo list again to find out which entry to delete
        entries = []
        with csv_path.open('r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) == 3:
                    entries.append(row)  # Store the entries

        # Check if the entry number is valid
        if 1 <= entry_number <= len(entries):
            # Confirm deletion with the user
            title = entries[entry_number - 1][0]  # Get the title of the entry to delete
            confirm_delete = input(f"Are you sure you want to delete the entry '{title}'? (Y/n): ").strip().lower()

            if confirm_delete == 'y':
                # Delete the entry by writing back the remaining entries
                with csv_path.open('w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Title', 'Description', 'Time Frame'])  # Write the header back
                    for i, row in enumerate(entries):
                        if i != entry_number - 1:  # Skip the entry to delete
                            writer.writerow(row)  # Write back all other entries
                print(f"Entry '{title}' deleted successfully.")
                user.decr_task()
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid entry number. Please try again.")

