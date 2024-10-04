# functions.py

import csv
from pathlib import Path
from classes import User

# Universal confirmation function to standardize user input code
def confirm():
    while True:  # Doesn't stop until the user enters Y/y or N/n
        userInput = input("Would you like to confirm? (Y/n): ").strip().lower()
        if userInput == 'y':
            return 'y'
        elif userInput == 'n':
            return 'n'
        else:
            print("Invalid input. Please enter Y or N: ")

def getUserInfo(user):
    configPath = Path("config.txt")
    variables = {}
    
    # Try to read the config file
    if configPath.exists():
        with open(configPath, 'r') as file:
            for line in file:  # Read each line and process it
                key, value = line.strip().split(" = ")
                variables[key] = value.strip("'")  # Remove the quotes
        
        # If the file exists, retrieve name and tasks
        name = variables.get('name', "")
        tasks = int(variables.get('tasks', 0))  # Ensure tasks is an integer
        user.name = name  # Set the user name from the config
        user.tasks = tasks  # Set the user tasks from the config
    else:
        # Create the config file with default values if it doesn't exist
        with open(configPath, 'w') as file:
            file.write("name = ''\n")  # Write a default entry
            file.write("tasks = 0\n")  # Initialize tasks as well
            print(f"Config file '{configPath}' created with default values.")
        
        # Prompt for user information since the file doesn't exist
        while user.name == "":
            print("This is your first time using the program, enter your name")  # Prints the result
            tempName = input("Please enter your name: ")
            print(f"Is your name '{tempName}'?")
            if confirm() == 'y':
                with open(configPath, 'w') as file:
                    file.write(f"name = '{tempName}'\n")  # Store the name in a proper format                
                    print(f"Thank you, {tempName}! You can proceed.")
                user.name = tempName  # Update the name after confirming
        user.tasks = 0  # Initialize tasks if file was created
    return user.name, user.tasks

def welcome(user):
    print(f"Welcome, {user.name}, to PyPlanner. You have {user.tasks} tasks stored.")

def menuLogic(user):
    print("What would you like to do?")
    while True:
        menuChoice = input("1: Write Todo 2: Short 3: Med 4: Long -- ")
        if menuChoice == '1':
            writeTodo(user)
        elif menuChoice in ['2', '3', '4']:
            readTodo(user, int(menuChoice))  # Convert to integer
        else:
            print("Please input a valid response.\n 1: Write Todo 2: Short 3: Med 4: Long -- ")

def writeTodo(user):
    csvPath = Path('todo.csv')

    # Check if the CSV file exists
    if not csvPath.exists():
        with open(csvPath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Description', 'Time Frame'])  # Write headers if the file didn't exist

    while True:
        # Prompt for todo details
        title = input("Enter the title: ")    
        desc = input("Enter the description: ")

        # Loop to ensure correct period input
        while True:
            period = input("Enter the time frame (s: short-term, m: medium-term, l: long-term): ").strip().lower()
            if period in ['s', 'm', 'l']:
                break
            else:
                print("Invalid entry. Please enter S, M, or L.")

        # Display the details and confirm
        print("Are you happy with the following entry?")
        print(f"---\nTitle: {title}\nDescription: {desc}\nPeriod: {period}\n---")
        
        if confirm() == 'y':
            # Save the todo to CSV
            with open(csvPath, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([title, desc, period])  # Append the todo item
            print("Todo added successfully!")
            user.incrTask()  # Increment the task count
            break
        else:
            print("Please redo your entry.")

def readTodo(user, menuChoice):
    # Map the menu choices to their respective time frames
    menuChoiceString = {2: "s", 3: "m", 4: "l"}
    
    # Get the corresponding time frame string
    time_frame = menuChoiceString.get(menuChoice)
    
    if time_frame is None:
        print("Invalid menu choice.")
        return
    
    csvPath = Path('todo.csv')
    if not csvPath.exists():
        print("No todo entries found. The todo.csv file does not exist.")
        return

    # Read from the CSV and filter based on the time frame
    with open(csvPath, 'r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip header row
        
        print(f"Reading {time_frame} To-dos:")
        found = False

        for row in reader:
            if len(row) == len(headers) and row[2].strip().lower() == time_frame:  # Ensure comparison is case-insensitive
                print(f"Title: {row[0]}, Description: {row[1]}, Time Frame: {row[2]}")
                found = True
            
        if not found:
            print(f"No {time_frame} To-dos found.")
            print("Would you like to make one?")
            if confirm() == 'y':
                writeTodo(user)
            else:
                menuLogic(user)
