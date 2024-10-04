# todo.py
from classes import User
from funcs import getUserInfo, welcome, menuLogic

# Create a User instance
user = User()

# Get user information and welcome them
name, tasks = getUserInfo(user)
welcome(user)
menuLogic(user)
