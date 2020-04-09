import sys
import os
import subprocess
from Display_Screen.Screen import Screen


#!Python 3
# This script it shows the currently enviroment variables, and checks if a path is added or not. 

screen = Screen('System variables manager')
screen.display()

if len(sys.argv) < 2:
    print("Usage: (path 'vars') print the current environment system variables")
    print("       (path 'path') check if the given path is added")
    sys.exit()

arg = sys.argv[1]

enviroment_vars = subprocess.check_output('echo %PATH%', shell = True)
paths_list = enviroment_vars.decode('utf-8').split(';')[:-1]

if arg == 'vars':
    for index,path in enumerate(paths_list,1):
        print(f'[{index}] -> {path}')

else:
    for path in paths_list:
        if path == arg:
            print('The path is added.')
            sys.exit()

    print("The path isn't added.")
    