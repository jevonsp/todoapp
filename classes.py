# classes.py

class User:
    def __init__(self, name='', tasks=0):
        self.name = name
        self.tasks = tasks

    def incrTask(self):
        self.tasks += 1
