from pathlib import Path

def startUp():
    configPath = Path("config.txt")
    variables = {}
    print("Welcome to PyPlanner")

    if not configPath.is_file():  # Checks if the configPath exists
        configPath.write_text("tasks = 0")  # Write default value
        print("This is your first time using the program, you have zero tasks.")  # Prints the result
    else:
        print("Welcome back!")  # Only print if the file exists
        # Read the config file
        with open(configPath, 'r') as file:
            exec(file.read(), variables)  # Execute the content in the variables context
        tasks = variables.get('tasks', 0)  # Retrieve the number of tasks safely
        print(f"You have {tasks} tasks.")  # Prints the result