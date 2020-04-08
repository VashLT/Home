import shelve
import os
import time
import sys
from Display_Screen.Screen import Screen

#! Python 3
# Task manager v1.0

def store_tasks():
    try:
        with shelve.open('Tasks') as task_file:
            index = 0
            if len(task_file) > 0:
                index = 0
                #print the store tasks
                for task,date in task_file.values():
                    index += 1
                    task_parse = f"[%s] {task}" % str(index)
                    info_date = f'added on {date}'.rjust(100-len(task_parse))
                    print(task_parse, info_date)
            else:
                print("No previous tasks availables.")
    except:
        print("[INFO] file couldn't be read.")

def add_task():
    try:
        with shelve.open('Tasks') as task_file:

            task_string = input('Enter the task: ')
            task = [task_string, time.strftime("%b %d at %H:%M", time.localtime())]
            #keys in the file are saved as Task (Number)
            task_file['Task %s' % str(len(task_file) + 1)] = task
            print("[INFO] the task was successfully added.")

    except ValueError:
        print("String value was expected.")

    except:
        print("[INFO] The program can't access to the file.")

def delete_task(num):
    try:
        with shelve.open('Tasks') as task_file:
            for key in task_file.keys():
                num -= 1
                if num == 0:
                    del task_file[key]
                    print("[INFO] The task was successfully deleted.")
                    return
            print("[INFO] The task wasn't found.")
    except:
        print("[INFO] The operation couldn't be completed.")
def selector(choose):
    screen.display()
    try:
        choose = int(choose)
        if choose == 1:
            add_task()
            time.sleep(1)
        elif choose == 2:
            try:
                store_tasks()
                num = int(input("Enter the num of the task: "))
                delete_task(num)
                time.sleep(1)
            except ValueError:
                print("A integer value is expected.")
        elif choose ==3:
            store_tasks()
            time.sleep(1)
        elif choose ==4:
            print("Thanks for using the script!")
            sys.exit()

    except ValueError:
        print("A number is expected.")



screen = Screen('Task manager')
screen.display()
if len(sys.argv) < 2:
    print('Usage: (task_manager 1) add a new task ')
    print('       (task_manager 2) delete a task ')
    print('       (task_manager 3) show tasks ')
    print('       (task_manager 4) exit ')
    sys.exit()
store_tasks()
time.sleep(2)
selector(sys.argv[1])
while True:    

    print('\n\nWhat do you want to do?')
    print('[1] -> Add a task.')
    print('[2] -> Delete a task. ')
    print('[3] -> Show tasks.')
    print('[4] -> Exit.')
    try:
        choose = input('Enter: ')
        selector(choose)
    except ValueError:
        print('A number is expected.')
        

