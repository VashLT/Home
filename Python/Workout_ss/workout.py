import sys, os, re, google_ss_color,gs, gspread, gspread_formatting, time, batch_class
import pyinputplus as pyip
from Display_Screen.Screen import Screen
from oauth2client.service_account import ServiceAccountCredentials
from datetime import timedelta, datetime

#! Python3

# Workout spreadsheet manager 
""" 
    This script allows fill in data about exercise stuff and info about my weight. The data is store
    in a google spreadsheet on the cloud.
"""

# pylint: disable=maybe-no-member
# pylint: disable=no-value-for-parameter
# pylint: disable=too-many-function-args

SPREADSHEET_NAME = "Workout"
DEFAULT_ROW = 6
DEFAULT_COLUMN = 2


class Workout():
    def __init__(self, *args):
        self.spreadsheet = gs.open_spread_sheet(SPREADSHEET_NAME)
        #Screen object to keep updating the main frame which shows the name of the script
        self.screen = Screen("Workout manager", version = "1.2") #3/05/2020
        self.options = ["fill", "add", "create", "check"]
        if len(args) < 2:
            self.usage()
        else:
            self.digest_args(*args)
    
    def usage(self):
        usage = """
            Usage: (workout fill)   - Input dialogue to prompt the data to fill
                   (workout add)    - Input dialogue to prompt the data to add
                   (workout create) - Create a body weight table
                   (workout check)  - Print the averague weight of a given week
            """
        print(usage)
        sys.exit()

    def digest_args(self, *args):
        self.screen.display()

        if args[1] == "create":
            #to make sure the given name is right
            while True:
                ans = pyip.inputYesNo(prompt= "Do you want to create a new sheet? (y/n)",yesVal="y", noVal = "n",limit = 3)
                sheet_name = pyip.inputStr("Enter the sheet name: ", limit = 3)
                if ans == "y":
                    try:
                        self.worksheet = self.spreadsheet.add_worksheet(title=sheet_name, rows ="100", cols="25")
                        break
                    except gspread.exceptions.APIError:
                        print(f'[INFO] A sheet with the name "{sheet_name}" already exists.')
                else:
                    try:
                        self.worksheet = self.spreadsheet.worksheet(sheet_name)
                        break
                    except gspread.exceptions.WorksheetNotFound:
                        print("[INFO] The sheet wasn't found.")

            self.create_table("Week 1", new = True)
            self.update_cloud([], (DEFAULT_ROW, DEFAULT_COLUMN))
            
        else:
            #FIND THE WORKSHEET AND THE CORRESPONDING WEIGHT TABLE
            try:
                sheet_name = input("Enter the name of the sheet: ").lower().capitalize()
                
                self.worksheet = self.spreadsheet.worksheet(sheet_name)

                self.week = pyip.inputInt("Enter the week number: ",limit = 3)
                print("[INFO] searching the week table...")

                coordinates = self.find_table(self.week) #return the location of the weight table

                if not coordinates:
                    print(f"[INFO] Previous week table wasn't found.")
                    ans = pyip.inputYesNo(prompt= "Do you want to create a new table? (y/n) ",yesVal="y", noVal = "n",limit = 3)
                    if ans == 'y':
                        self.create_table("Week 1", new = True)
                else:
                    print("[INFO] Week table found succesfully.")

                #this is intended to handle with add, check, fill and create
                self.update_cloud(args[1], coordinates)

            except gspread.exceptions.WorksheetNotFound:
                print("[INFO] The sheet wasn't found.")
                
                ans = pyip.inputYesNo(prompt= "Do you want to create a new sheet? (y/n)",yesVal="y", noVal = "n",limit = 3)
                if ans == 'n':
                    sys.exit()
                self.worksheet = self.spreadsheet.add_worksheet(title=sheet_name, rows ="100", cols="25")

            except pyip.RetryLimitException:
                print("[INFO] Limit of attempts exceeded.")
            #a little break to read the information
            time.sleep(1.5)



    def update_cloud(self, do, location):
        try:
            while True:
                if do == 'create':
                    #this handles with a sheet which has previous weight tables
                    prev_table_coord = None
                    limit = 4 #max 4 weight tables per sheet
                    #search for the previous table, max number of weeks per month is 4
                    while not prev_table_coord: 
                        prev_table_coord = self.find_table(week = limit) 
                        limit -= 1
                        if limit == 0:
                            raise Exception("[INFO] The current sheet has no weight tables.")

                    coord = (prev_table_coord[0]+ 8 , prev_table_coord[1])
                    week = limit + 2
                    self.create_table(coord[0], coord[1],f"Week {self.week}") 
                    print("[INFO] The table was created succesfully.")      

                elif do == "check":

                    row = location[0] + 1
                    col = location[1] 

                    first_day= self.worksheet.cell(row, col).value
                    finish_day = self.construct_dates(first_day, single_mode = True)
                    prom_weight = self.worksheet.cell(row , col + 3).value
                    print(f"The prom weight during the week {first_day}~{finish_day} is {prom_weight} kg")
                
                elif do == "fill" or do == "add":
                    data = ["weight", "body fat %", "calories per day"] #categories to manipulate
                    self.screen.display()

                    for index, kind in enumerate(data,1): #shows the categories
                        print(f"[{index}] - > {kind}")

                    opc = pyip.inputInt("Enter: ", greaterThan=0,max = len(data), limit = 3)

                    mssg = data[opc - 1]

                    if do == "fill":
                        data = []
                        for index in range(7):
                            value = pyip.inputFloat(f"[{index + 1}] Enter the {mssg}: ", limit = 3, min=0, blank=True)
                            if value == "":
                                break
                            data.append(value)

                        if opc == 1:
                            self.fill_data(location[0] + 1, location[1] + 1, data)
                        elif opc == 2:
                            self.fill_data(location[0] + 1, location[1] + 2, data)
                        elif opc == 3:
                            self.merge(location[0]+1, location[1] + 4)
                            self.add(location[0]+1, location[1] + 4, data[0]) #only working with one value

                        print(f"[INFO] {mssg} data filled succesfully.")

                    elif do == "add":
                        value = pyip.inputFloat(f"Enter the {mssg}: ",limit = 3)
                        if opc == 1:
                            row = location[0] + 1
                            col = location[1] + 1
                        elif opc == 2:
                            row = location[0] + 1
                            col = location[1] + 2
                        elif opc == 3:
                            row = location[0] + 1
                            col = location[1] + 4
                            self.merge(row,col)

                        try:
                            self.add(row,col,value)
                            print(f"[INFO] {mssg} added succesfully.")
                        except Exception as ex:
                            print(f"[INFO] {ex.args[0]} - {mssg} data couldn't be added.")
                time.sleep(1.5)        

                #this implies is the first modification
                if "Change Sheet" not in self.options:
                    ans = pyip.inputYesNo(f"Do you want to do anything else? (y/n) ",yesVal="y", noVal="n", limit=3)
                    if ans != "y":
                        print("Thanks for using the script!.")
                        sys.exit()
                    self.options.append("Change Sheet")
                    self.options.append("Exit")

                self.screen.display()

                for index,option in enumerate(self.options, 1):
                    print(f"[{index}] {option}")
                opc = pyip.inputInt("Enter: ", limit = 3, min = 1, max = len(self.options))
                #this mean the user has typed the exit option
                if opc == len(self.options):
                    print("Thanks for using the script!.")
                    sys.exit()
                do = self.options[opc - 1 ]
                if do == "Change Sheet":
                    self.digest_args(*("Workout", "Change Sheet"))

        except pyip.RetryLimitException:
            print("[INFO] Number attempts exceeded.")
        except gspread.exceptions.CellNotFound:
            print(f"[INFO] Previous week table wasn't found.")     
        except Exception as ex:
            print(f"{ex.args[0]}")

    def create_table(self, title, row  = DEFAULT_ROW,col = DEFAULT_COLUMN,new = False):
        print("[INFO] Creating the weight table...")
        table = self.body_weight_table(row, col,title)
        self.spreadsheet.batch_update(table.get_body())
        
        if new: #for a just created sheet it's necessary a initial date
            initial_date = input("Enter the initial date (dd/mm/yyy): ")
        
        else:
            form = r"%d/%m/%Y" #DD/MM/YY
            raw_date = datetime.strptime(self.worksheet.cell(row-1,col).value,form) + timedelta(days = 1) #search for the corresponding initial day in the previous body weight table
            initial_date = raw_date.strftime(form)

        dates_to_fill = self.construct_dates(initial_date)

        print("[INFO] Filling the dates...")
        self.fill_data(row+1, col, dates_to_fill)
        print("[INFO] Dates filled succesfully.")
        #update the current working week
        self.week = [int(char) for char in title.split() if char.is_digit()][0]
        print("[INFO] The weight table was created succesfully.")
    
    def find_table(self, week):
        try:
            cell_match = self.worksheet.find("Week %s" % str(week))
            location = (cell_match.row , cell_match.col) #coords (x,y)
            return location
        except gspread.CellNotFound:
            return None
    
    #data must be an iterable object
    def fill_data(self, row,column,data):
        assert hasattr(self, "worksheet")
        for value in data:
            self.worksheet.update_cell(row, column, value)
            row += 1
    
    #Calculate the dates of the start day's preceding days
    def construct_dates(self, start_day, single_mode = False):
        form = r"%d/%m/%Y" #dd/mm/yyyy format
        dates = []
        raw_date = datetime.strptime(start_day, form)
        if single_mode:
            finish_day = raw_date + timedelta(days = 6)
            return finish_day.strftime(form)
        for day in range(7):
            date = raw_date + timedelta(days = day) #roam the days

            dates.append(date.strftime(form))
        
        return dates
    
    def add(self, row,column,value):
        cell = self.worksheet.cell(row,column)
        cont = 0
        while cell.value != '':
            #a column has max 7 values
            cont += 1
            if cont > 6:
                raise Exception("The column is full")
            cell = self.worksheet.cell(row + cont,column)
        self.worksheet.update_cell(cell.row, cell.col, value)

    def merge(self,row,col):
        table = batch_class.batch_dealing(self.worksheet._properties['sheetId'])
        table.merge_cells(row,row+6,col,col)
        self.spreadsheet.batch_update(table.get_body())

    def body_weight_table(self,start_row,start_col, title):
        assert hasattr(self, "worksheet")
        palette_colors = ['LIGHT YELLOW 3','LIGHT RED 3','LIGHT ORANGE 3','LIGHT PURPLE 2','LIGHT RED BERRY 3']
        #table dimentions
        s_row = start_row
        e_row = start_row + 8
        s_col = start_col
        e_col = start_col + 4

        #create an instance of batch_dealing class
        table = batch_class.batch_dealing(self.worksheet._properties['sheetId'])

        #title cell

        table.merge_cells(s_row, s_row, s_col, e_col)
        self.worksheet.update_cell(s_row,s_col,title)


        #it gives color to the columns
        for row in range(s_row+1, e_row):
            index = 0
            for column in range(s_col, e_col+1):
                if column == s_col:
                    table.set_date_format(row,column)

                if column == s_col+1 or column == s_col+2:
                    table.set_number_format(row,column)

                table.set_color( google_ss_color.rgb( palette_colors[index] ), row, column)
                table.font_size(10, row, column, bold = True)
                table.set_borders((0,0,0), "SOLID", row, column)
                index += 1

        #Prom column weight    
        table.merge_cells(s_row+1, e_row-1, e_col-1, e_col-1)
        col = gs.column_type[start_col+1]
        self.worksheet.update_cell(s_row+1, e_col-1,f'=PROMEDIO({col}{s_row+1}:{col}{e_row-1})')  #add the formule


        table.font_size(10, s_row, s_col, bold = True)
        table.set_borders_range((0,0,0), "SOLID", s_row,s_row,s_col,e_col)
        table.set_color( google_ss_color.rgb('LIGHT CORNFLOWER 2'), s_row, s_col)
        #setting the alignment
        table.alignment_range("CENTER",s_row, e_row,s_col, e_col)

        return  table    

if __name__ == "__main__":
    Workout(*sys.argv)