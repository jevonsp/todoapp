# classes.py
from pathlib import Path
from typing import Dict

class User:
    def __init__(self, name: str = '', tasks: int = 0):
        self.name = name
        self.tasks = tasks
        self.config_path = Path("config.txt")

    def incr_task(self) -> None:
        """Increment the task count and update the configuration."""
        self.tasks += 1
        self.update_config()

    def decr_task(self) -> None:
        """Decrement the task count and update the configuration."""
        self.tasks -= 1
        self.update_config()
        if self.tasks < 0:
            self.tasks = 0
            self.update_config()

    def update_config(self) -> None:
        """Update the configuration file with current user data."""
        config = self.read_config()
        config['name'] = self.name
        config['tasks'] = str(self.tasks)
        self.write_config(config)

    def read_config(self) -> Dict[str, str]:
        """Read the configuration file and return as a dictionary."""
        config = {}
        if self.config_path.exists():
            with self.config_path.open('r') as file:
                for line in file:
                    key, value = line.strip().split(" = ")
                    config[key] = value.strip("'")
        return config

    def write_config(self, config: Dict[str, str]) -> None:
        """Write the configuration dictionary to the config file."""
        with self.config_path.open('w') as file:
            for key, value in config.items():
                file.write(f"{key} = '{value}'\n")
