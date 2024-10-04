from pathlib import Path

def getUserInfo():
    configPath = Path("config.txt")
    variables = {}
    # Tries to read the config files
    if configPath.exists():
        with open(configPath, 'r') as file:
            exec(file.read(), variables)  # Execute the content in the variables context

    name = variables.get('name', "")

    if name == "":
        print("This is your first time using the program, enter your name")  # Prints the result
        while True:
            tempName = input("Please enter your name: ").strip()
            
            # Ask the user if they want to continue
            confirmation = input(f"Is your name '{tempName}'? (y/n): ").strip().lower()
            
            if confirmation == 'y':
                with open(configPath, 'w') as file:
                    file.write(f"name = '{tempName}'\n")  # Store the name in a proper format                
                    print(f"Thank you, {name}! You can proceed.")
                break  # Exit the loop if the user confirms
            elif confirmation == 'n':
                print("Let's try again.")
            else:
                print("Invalid input. Please enter 'y' for Yes or 'n' for No.")
