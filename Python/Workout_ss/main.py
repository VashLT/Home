import sys, gspread, time
import pyinputplus as pyip
from My_modules.Screen.Screen import Screen
from workout import *

#! Python 3

# spreadsheet manager

""" 
    This script allows fill in data about exercise stuff and info about my weight. The data is store
    in a google spreadsheet on the cloud.
"""

#TODO: solve issue can't create new table, week number is wrong.

class Menu():
    def __init__(self, workout):
        """ Allows a better experience while selecting options """
        self.workout = workout
        self.sheets = workout.sheets #list of all the sheet names
        self.screen = Screen("Workout manager", version = "1.2") #15/06/2020
        self.options = ["Add","Fill","create table","check weight","Show table","Create sheet","Change sheet","Change week","Exit"]
    
    def usage(self):
        usage = """
            Usage: (workout fill)   - Input dialogue to prompt the data to fill
                   (workout add)    - Input dialogue to prompt the data to add
                   (workout create) - Create a body weight table
                   (workout check)  - Print the averague weight of a given week
                   (workout table)  - Print the current table data on command line
            """
        print(usage)
        sys.exit()

    def input_week(self, create = False):
        """ get by prompt the week to work with""" 
        assert hasattr(self.workout, 'worksheet')
        if create:
            self.workout.create_table(title="Week %s" % str(1), new = True) #initialize a new table
            return 1
        limit = 3 #max 3 iterations
        while True: #till input an existent week
            if limit == 0:
                return 
            try:
                week = pyip.inputInt("Enter week (number): ",limit=3, min=0, max=4)
                coord = self.workout.find_table(week)
            except pyip.RetryLimitException:
                print(f"[INFO] Limit of attempts exceeded.")
                return
            if coord: #found a week table
                self.workout.location = coord
                return week
            else:
                print(f"[INFO] There's no such a table for week {week}")
            limit -= 1

    def get_workspace(self,create = False,only_week = False):
        """ select worksheet and week
            week: tables inside a sheet are found by a week number
                    this number is according to the month, so max number is 4.
            only_week: intended to allow swiching only between tables 
            create: False stands for only select an existent sheet
        """
        try:
            if only_week:
                week = self.input_week()
            else:
                while True: #till select a sheet, or create a new one
                    sheet_name = pyip.inputStr("Enter the name of the sheet: ", limit=3).lower().capitalize()
                    print("[IN PROGRESS] Searching sheet ...")
                    if sheet_name in self.sheets:
                        if create:
                            print(f"[INFO] Already exists a sheet with name {sheet_name}")
                        #by default select the target sheet regardless if create is True
                        print("[INFO] Sheet succesfully located.")
                        break
                    else:
                        if create:
                            self.workout.create_sheet(sheet_name)
                        else:
                            print(f"[INFO] There's no such a sheet called {sheet_name}")
                            self.workout.show_sheets()
                self.workout.set_worksheet(sheet_name)
                week = self.input_week(create= create)
            if not week:
                return False
            self.workout.week = week    
            return True          
        except pyip.RetryLimitException:
            print(f"[INFO] Limit of attempts exceeded.")
            return False
        except Exception as ex:
            print(f"[ERROR] Something was wrong - {type(ex)} - {ex}")
            return False

    def interface(self, init_opc = 0):
        response = self.get_workspace()
        if not response: #assure the workspace is initialized correctly
            return
        while True:
            try:
                self.screen.display()
                num_opc = len(self.options)
                for index,opc in enumerate(self.options, 1):
                    print(f"[{index}] {opc} ")
                if init_opc != 0: #allow arg to avoid input-typing
                    ans = init_opc
                else:
                    ans = pyip.inputInt("Opción: ", limit = 3, min = 1, max = num_opc)
                if ans == num_opc:
                    return
                self.digest_opc(ans)
                init_opc = 0 #next decitions must be input from keyboard
                input('Press enter to continue ...')               
            except pyip.RetryLimitException:
                print(f"[ERROR] Limite de intentos excedido.")
    
    def digest_opc(self, option):
        self.screen.display()
        if option == 3: #create table
            """ create a table independent of the input week number
                this avoid overwrite tables.
            """
            assert hasattr(self.workout, "week")
            prev_coord, week = self.workout.get_previous_table_coord() #returns coord, week
            assert prev_coord
            if week < 4:
                title = "Week %s" % str(week + 1)
                row, col = prev_coord[0] + 8, prev_coord[1] #(row, col)
                self.workout.create_table(title=title, row=row, col=col)
            else:
                print(f"[INFO] Numbers of tables per sheet exceeded. Please create a new sheet.")

        elif option == 4: #show prom weight during the week
            location = self.workout.location
            row = location[0] + 1
            col = location[1]
            first_day = self.workout.worksheet.cell(row, col).value
            finish_day = self.workout.construct_dates(first_day, single_mode = True)
            prom_weight = self.workout.worksheet.cell(row, col + 3).value
            print(f"The prom weight during the week {first_day}~{finish_day} is {prom_weight} kg")
        
        elif option == 5: #show a diagram of the current table
            table = self.workout.construct_table()
            print(table)

        elif option == 6: #create sheet
            self.get_workspace(create=True)

        elif option == 7: #change sheet
            self.get_workspace()

        elif option == 8: #change week
            self.get_workspace(only_week=True)

        else: #add and fill
            fields = self.workout.fields
            for index, field in enumerate(fields.keys(), 1):
                print(f"[{index}] -> {field}")

            ans = pyip.inputInt("Option: ", limit = 3, min = 1, max = len(fields))
            #get num of units to move 
            field_names = list(fields.keys())
            index = ans - 1
            step = fields[ field_names[index] ] 
            location = self.workout.location
            row = location[0] + 1
            col = location[1] + step
            #dialog
            mssg = field_names[index]
            if option == 1: # add 
                try:
                    value = pyip.inputFloat(f"Enter the {mssg}: ",limit = 3)
                except pyip.RetryLimitException:
                    print(f"[INFO] Limit of attempts exceeded.")
                if ans == len(fields) - 1: #to update prom weight is necessary merge cells
                    self.workout.merge(row, col)
                
                response = self.workout.add(row, col, value)
                if not response:
                    print(f"[ERROR] The column is full.")
                else:
                    print(f"[INFO] {mssg} added succesfully.")
            
            elif option == 2: #fill
                data = []
                for index in range(1,8):
                    try:
                        value = pyip.inputFloat(f"Enter the {mssg}: ",limit = 5, min=0, blank=True)
                    except pyip.RetryLimitException:
                        print("Limit of attempts excedeed.")
                        break
                    if value == '':
                        break
                    data.append(value)
                if ans == len(fields) - 1: #to update prom weight is necessary merge cells
                    self.workout.merge(row, col)
                    data = data[0] #only working with one value
                temp_location = (row, col)
                #fill cells
                for index, value in enumerate(data):
                    result = self.workout.add(row, col, value)
                    if not result:
                        print("[ERROR] The column is full. Next values couldn't be added:")
                        print(f"                            {data[index:]}")
                        break
                print(f"[INFO] {mssg} data filled succesfully.")
                
        time.sleep(1)




def main(args):
    opc = 0
    if "table" in args:
        opc = 5
    workout = Workout()   
    menu = Menu(workout)
    if len(args) < 2:
        menu.usage()
    else:
        menu.interface(init_opc = opc)
    print("Thanks for using the script! ")


if __name__ == "__main__":
    main(sys.argv)
