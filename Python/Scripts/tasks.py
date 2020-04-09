import shelve
import os
import time
import sys
from Display_Screen.Screen import Screen

#! Python 3
# Task manager v1.0

class Node():
    def __init__(self, task, date):
        self.index = 0
        self.task = task
        self.date = date
        self.next = None

class Task_list():
    def __init__(self):
        self.head = None

    def __del__(self):
        while self.head is not None:
            aux = self.head
            self.head = self.head.next
            print(f"[INFO] Freeing memory  {aux}")
            aux = None 

    def get_tail(self): #return the last task added and update the indexes of the task list.
        index = 1
        if self.head is not None:
            traveller = self.head
            while traveller is not None:
                try:
                    traveller.index = index #update all the indexes
                    if traveller.next is None:
                        return traveller
                    traveller = traveller.next
                    index += 1
                except TypeError:
                    print("[INFO] A problem has appeared, task list is wrong.")
        else:
            return self.head

    def show_task_list(self):
        
        if self.head is None:
            print("[INFO] No previous tasks available.")
            return

        traveller = self.head
   
        while traveller is not None:
            task_parse = f"[%s] {traveller.task}" % str(traveller.index)
            info_date = f'added on {traveller.date}'.rjust(100-len(task_parse))
            print(task_parse, info_date)
            traveller = traveller.next

    def query_task(self,node = None, index= -1):
        if self.head is not None:
            if node == self.head:
                return traveller

            traveller = self.head

            if index < 1:
                while traveller is not None:
                    try:
                        if traveller.next is None:
                            print("[INFO] The task to delete isn't in the list.")
                            return None
                        if traveller.next == node:
                            return traveller #return the previous task to the task asked
                        traveller = traveller.next

                    except TypeError:
                        print("[INFO] The task couldn't be deleted.")
            #non-negative index
            else:
                if index == 1:
                    return self.head
                while traveller is not None:
                    try:
                        if traveller.next is None:
                            print("[INFO] The task to delete isn't in the list.")
                            return None
                        elif traveller.next.index == index:
                            return traveller
                        traveller = traveller.next
                    except TypeError:
                        print("[INFO] The task couldn't be deleted.") 
        else:
            return self.head
                    
    def add_task(self, node):
        try:
            if self.head != None:
                tail = self.get_tail()
                tail.next = node
                node.index = tail.index + 1
            #add the first task to the task list
            else:
                node.index = 1
                self.head = node
                self.update_file() #update the shelve dictionary
            print("[INFO] The task was added succesfully.")
        except TypeError:
            print("[INFO] The task wasn't added succesfully.")
    
    def remove_task(self,index):
        prev_task = self.query_task(index = index)
        if prev_task == self.head:
            if index == 1: #the task to delete is the first one
                task_to_delete = self.head
                self.head = self.head.next
            else: #otherwise, task to delete is the next to the first one
                task_to_delete = self.head.next
                self.head.next = self.head.next.next

        elif prev_task is not None:
            #break the connections of task_to_delete
            task_to_delete = prev_task.next
            merge = task_to_delete.next
            prev_task.next = merge

        else:
            return

        del task_to_delete

        self.get_tail() #update the indexes
        self.update_file() #update the shelve file

        print("[INFO] The task was removed succesfully.")
    
    def update_file(self):
        path = os.path.join(os.path.expanduser('~'),'jose2','Documents','Tasks')
        with shelve.open(path) as sfile:
            sfile["Task list"] = self.head
            sfile.close()
    


def store_tasks(task_list):
    try:
        path = os.path.join(os.path.expanduser('~'),'jose2','Documents','Tasks')
        with shelve.open(path) as task_file:
            first_task = task_file['Task list']

            if  first_task is not None:
                #print the store tasks and fill the task_list instance
                temp = first_task
                
                while temp is not None:
                    task_parse = f"[%s] {temp.task}" % str(temp.index)
                    info_date = f'added on {temp.date}'.rjust(100-len(task_parse))
                    print(task_parse, info_date)
                    temp = temp.next
                #assign the stored node to the "current" task list
                task_list.head = first_task
            else:
                print("[INFO] No previous tasks availables.")
    except KeyError:
        print("[INFO] File couldn't read, no previous tasks availables.")

def fill_task():
    try:
        task = input('Enter the task: ')
        task_date = time.strftime("%b %d at %H:%M", time.localtime())

        current_task = Node(task, task_date)

        return current_task

    except ValueError:
        print("String value was expected.")
 
        
def selector(choose,task_list):
    screen.display()
    try:
        choose = int(choose)
        if choose == 1:
            task = fill_task()
            task_list.add_task(task)
            time.sleep(1)
        elif choose == 2:
            try:
                task_list.show_task_list()
                num = int(input("Enter the num of the task: "))
                task_list.remove_task(num)
                time.sleep(1)
            except ValueError:
                print("A integer value is expected.")
        elif choose ==3:
            task_list.show_task_list()
            time.sleep(1)

    except ValueError:
        print("A number is expected.")



screen = Screen('Task manager')
screen.display()

task_list = Task_list()

if len(sys.argv) < 2:
    print('Usage: (task_manager 1) add a new task ')
    print('       (task_manager 2) delete a task ')
    print('       (task_manager 3) show tasks ')
    print('       (task_manager 4) exit ')
    sys.exit()
store_tasks(task_list)
time.sleep(2)
selector(sys.argv[1], task_list)
while True:    

    print('\nWhat do you want to do?')
    print('[1] -> Add a task.')
    print('[2] -> Delete a task. ')
    print('[3] -> Show tasks.')
    print('[4] -> Exit.')
    try:
        choose = input('Enter: ')
        if choose == '4':
            print("Thanks for using the script!")
            break
        selector(choose, task_list)
           
    except ValueError:
        print('A number is expected.')
        

