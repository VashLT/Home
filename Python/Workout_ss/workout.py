import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_formatting
import re
import batch_class
import gs
import google_ss_color
import sys, os
from Display_Screen.Screen import Screen
from datetime import timedelta, datetime
import pyinputplus as pyip
#! Python3
# Workout spreadsheet manager - This script allows fill in data about exercise stuff and info about my weight.


# pylint: disable=maybe-no-member
# pylint: disable=no-value-for-parameter
# pylint: disable=too-many-function-args

SPREADSHEET_NAME = "Workout"

ss = gs.create_spread_sheet(SPREADSHEET_NAME)
worksheet = ss.sheet1 #by default sheet number one

def get_spreadsheet_id_from_url(url):
    id_regex = re.compile(r'/spreadsheets/d/([a-zA-Z0-9-_]+)')
    sheet_id = id_regex.findall(url)
    return sheet_id[0]

def body_weight_table(start_row,start_col, title):
    palette_colors = ['LIGHT YELLOW 3','LIGHT RED 3','LIGHT ORANGE 3','LIGHT PURPLE 2','LIGHT RED BERRY 3']
    #table dimentions
    s_row = start_row
    e_row = start_row+8
    s_col = start_col
    e_col = start_col+4

    #create an instance of batch_dealing class
    table = batch_class.batch_dealing(worksheet._properties['sheetId'])

    #title cell

    table.merge_cells(s_row, s_row, s_col, e_col)

    #it gives color to the columns
    for row in range(s_row+1, e_row):
        cont = 0
        for column in range(s_col, e_col+1):
            if column == s_col:
                table.set_date_format(row,column)

            if column == s_col+1 or column == s_col+2:
                table.set_number_format(row,column)

            table.set_color( google_ss_color.rgb( palette_colors[cont] ), row, column)
            cont += 1
            table.font_size(10, row, column, bold = True)
            table.set_borders((0,0,0), "SOLID", row, column)
    
    table.merge_cells(s_row+1, e_row-1, e_col-1, e_col-1)
    col = gs.column_type[start_col+1]
    #adding the formule
    worksheet.update_cell(s_row+1, e_col-1,f'=PROMEDIO({col}{s_row+1}:{col}{e_row-1})')

    worksheet.update_cell(s_row,s_col,title)
    table.font_size(10, s_row, s_col, bold = True)
    table.set_borders_range((0,0,0), "SOLID", s_row,s_row,s_col,e_col)
    table.set_color( google_ss_color.rgb('LIGHT CORNFLOWER 2'), s_row, s_col)
    #setting the alignment
    table.alignment_range("CENTER",s_row, e_row,s_col, e_col)

    return  table

def fill_in(row,column,data):

    for value in data:
        worksheet.update_cell(row, column, value)
        row += 1

def match_table(number):
    cell_match = worksheet.find("Week %s" % str(number))
    location = [cell_match.row , cell_match.col]
    return location

#it calculates the corresponding week dates according to a given day
def parse_date(start_day, single_mode = False):
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

def add(row,column,value):
    cell = worksheet.cell(row,column)
    cont = 0
    while cell.value != '':
        cont += 1
        cell = worksheet.cell(row + cont,column)
        if cont > 7:
            print("[INFO] The column is full.")
            return
    worksheet.update_cell(cell.row, cell.col, value)

def create_table(row,col,title,new = False):
    table = body_weight_table(row, col,title)
    ss.batch_update(table.get_body())
    
    if not new: #new is True when the current sheet was just created
        form = r"%d/%m/%Y"
        raw_date = datetime.strptime(worksheet.cell(row-1,col).value,form) + timedelta(days = 1)
        initial_date = raw_date.strftime(form)
    else:
        initial_date = input("Enter the initial date (dd/mm/yyy): ")

    dates_to_fill = parse_date(initial_date)

    print("[INFO] Filling the dates...")
    fill_in(row+1, col, dates_to_fill)
    print("[INFO] Dates field filled succesfully.")

def merge(row,col):
    table = batch_class.batch_dealing(worksheet._properties['sheetId'])
    table.merge_cells(row,row+6,col,col)
    ss.batch_update(table.get_body())
    

#TODO solve problem not found a previous week table in a new sheet and get into an infinity loop.
def main():
    global worksheet

    screen = Screen("Workout spreadsheet manager")
    screen.display()

    options = ["fill", "create", "check", "update","add"]
    new_state = False
    if len(sys.argv) < 2 or sys.argv[1] not in options:
        print("Usage: (workout fill)   - Input dialogue to prompt the data to fill")
        print(       "(workout add)    - Input dialogue to prompt the data to add")
        print(       "(workout create) - Create a body weight table")
        print(       "(workout check)  - Print the averague weight of a given week")
        print(       "(workout update) - Input dialogue to prompt the data to update")

        sys.exit()

    choice = sys.argv[1]
    choice = choice.lower()

    try:
        sheet = input("Enter the name of the sheet: ")

        sheet = sheet.lower().capitalize()
        worksheet = ss.worksheet(sheet)
    except gspread.exceptions.WorksheetNotFound:
        print("[INFO] The sheet wasn't found.")
        try:
            ans = pyip.inputYesNo(prompt= "Do you want to create a new sheet? (y/n)",yesVal="y", noVal = "n",limit = 3)
            if ans == 'n':
                sys.exit()
        except pyip.RetryLimitException:
            print("[INFO] Number attempts exceeded.")
            sys.exit()

        worksheet = ss.add_worksheet(title=sheet, rows ="100", cols="25")
        new_state = True #when a new sheet is created.
    except:
        print("[INFO] Something was wrong.")
    
    if choice == 'create':
        try:
            while True:
                if new_state:
                    week=1
                    new_coord = [6,2] #row, column by default in a new sheet    
                    break

                week = int(input("Enter the week number: "))
                try:
                    prev_table_coord = match_table(week-1)
                    new_coord = [prev_table_coord[0]+ 8 , prev_table_coord[1]]
                    break
                except gspread.exceptions.CellNotFound:
                    print(f"[INFO] Previous week table wasn't found.")

            if new_state:
                create_table(new_coord[0], new_coord[1],f"Week {week}", new = True)
            else:
                create_table(new_coord[0], new_coord[1],f"Week {week}")

            print("[INFO] The table was created succesfully.")           

        except ValueError:
            print("[INFO] Table couldn't be created, a number is expected.")
        except KeyboardInterrupt:
            print("Thanks for using the script!.")
        except:
            print("[INFO] Something was wrong, table incompleted.")

    else:
        data = ["weight", "body fat %", "calories per day"]
        for index, kind in enumerate(data,1):
            print(f"[{index}] - > {kind}")
        try:
            choose = int(input("Enter: "))
            mssg = data[choose-1]

            week = int(input("Enter the week: "))
            print("[INFO] searching the week table...")

            try:
                coord = match_table(week)
                print("[INFO] Week table found succesfully.")
                if choice == "fill":
                    stuff = []
                    while True:
                        indx=1
                        value = float(input(f"[{indx}] Enter the {mssg}: "))
                        if value == 0:
                            break
                        stuff.append(value)
                        indx += 1
                        if len(stuff) == 7:
                            break
                    if choose == 1:
                        fill_in(coord[0] + 1, coord[1] + 1,stuff)
                    elif choose == 2:
                        fill_in(coord[0] + 1, coord[1] + 2,stuff)
                    elif choose == 3:
                        merge(coord[0]+1, coord[1] + 4)
                        add(coord[0]+1, coord[1] + 4, stuff[0])
                    print(f"[INFO] {mssg} data filled succesfully.")
                elif choice == 'check':
                    row = coord[0] +1
                    col = coord[1] 
                    date= worksheet.cell(row, col).value
                    finish_day = parse_date(date, single_mode = True)
                    prom_weight = worksheet.cell(row , col + 3).value
                    print(f"The prom weight during the week {date}~{finish_day} is {prom_weight} kg")

                elif choice == "add":
                    value = float(input(f"Enter the {mssg}: "))
                    if choose == 1:
                        row = coord[0]+1
                        col = coord[1]+1
                    elif choose ==2:
                        row = coord[0]+1
                        col = coord[1]+2
                    elif choose ==3:
                        row = coord[0]+1
                        col = coord[1]+4
                        merge(row,col)

                    add(row,col,value)
                    print(f"[INFO] {mssg} added succesfully.")

            except gspread.exceptions.CellNotFound:
                    print(f"[INFO] Previous week table wasn't found.")
                    try:
                        ans = pyip.inputYesNo(prompt= "Do you want to create a new table? (y/n) ",yesVal="y", noVal = "n",limit = 3)
                        if ans == 'n':
                            sys.exit()
                        else:
                            create_table(6,2,"Week 1", new = True)
                            
                        print("[INFO] The table was created succesfully.")

                    except pyip.RetryLimitException:
                        print("[INFO] Number attempts exceeded.")
                        sys.exit()
                    # except:
                    #     print("[INFO] Something was wrong, the table couldn't be created.")

        except ValueError:
            print("A number is expected.")
    
    sys.exit()

main()
