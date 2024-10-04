from funcs import getUserInfo, welcome, menuLogic

name, tasks = getUserInfo()
welcome(name, tasks)
menuLogic()
