import csv
from pathlib import Path

def getUserInfo():
    configPath = Path("config.txt")
    variables = {}
    # Tries to read the config files
    if configPath.exists():
        with open(configPath, 'r') as file:
            exec(file.read(), variables)  # Execute the content in the variables context
    else:
        # Create the config file with default values if it doesn't exist
        with open(configPath, 'w') as file:
            file.write("name = ''\n")  # Write a default entry
            print(f"Config file '{configPath}' created with default values.")

    name = variables.get('name', "")
    tasks = variables.get('tasks', 0)

    if name == "":
        print("This is your first time using the program, enter your name")  # Prints the result
        while True:
            tempName = input("Please enter your name: ").strip()
            
            # Ask the user if they want to continue
            confirmation = input(f"Is your name '{tempName}'? (Y/N): ").strip().lower()
            
            if confirmation == 'y':
                with open(configPath, 'w') as file:
                    file.write(f"name = '{tempName}'\n")  # Store the name in a proper format                
                    print(f"Thank you, {name}! You can proceed.")
                break  # Exit the loop if the user confirms
            elif confirmation == 'n':
                print("Let's try again.")
            else:
                print("Invalid input. Please enter 'yY' for Yes or 'N' for No.")
    else:
        print(f"Welcome back {name}! You have {tasks} tasks")

def menuLogic():
    print("What would you like to do?")
    while True:
        menuChoice = input("1: Write Todo 2: Short 3: Med 4: Long -- ")
        if menuChoice == '1':
            writeTodo()
        elif menuChoice == [2, 3, 4]:
            readTodos(menuChoice)
        else:
            print("Please input a valid response.\n 1: Write Todo 2: Short 3: Med 4: Long -- ")

def writeTodo():
    path = Path('todo.csv')

    # Check if the CSV file exists
    if not path.exists():
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Description', 'Time Frame'])  # Write headers if the file didn't exist

    while True:
        # Prompt for todo details
        title = input("Enter the title: ")    
        desc = input("Enter the description: ")
        period = input("Enter the time frame: ")
        
        print("Are you happy with the following entry?")
        print(f"---\n{title}\n{desc}\n{period}\n---\n")

        # Confirm the entry
        confirmation = input("Enter Y to confirm or N to redo: ").strip().lower()
        if confirmation == 'y':
            with open(path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([title, desc, period])  # Append the todo item
            print("Todo added successfully!")
            break  # Exit the loop after confirming
        elif confirmation == 'n':
            print("Redo your entry.")
        else:
            print("Please enter a valid response. Y to confirm and N to redo.")

def readTodos(menuChoice):
    choiceInt = int(menuChoice)
    menuChoiceString = {2:"short-term", 3: "medium-term", 4: "long-term"}
    print(f"Reading {menuChoiceString[choiceInt]} To-dos")