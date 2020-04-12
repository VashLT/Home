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
#! Python3
# Workout spreadsheet manager - This script allows fill in data about exercise stuff and info about my weight.


# pylint: disable=maybe-no-member
# pylint: disable=no-value-for-parameter
# pylint: disable=too-many-function-args

SPREADSHEET_NAME = "Workout"
SHEET_NAME = "Marzo"

ss = gs.create_spread_sheet(SPREADSHEET_NAME)
worksheet = ss.worksheet(SHEET_NAME)

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




def main():
    screen = Screen("Workout spreadsheet manager")
    screen.display()

    # if len(sys.argv) < 2:
    #     print("""Usage: (workout fill)   - Input dialogue to prompt the data to fill
    #                     (workout create) - Create a body weight table
    #                     (workout check)  - Print the averague weight of a given week
    #                     (workout update) - Input dialogue to prompt the data to update
    #     """)
    #     sys.quit()

    choice = input("Enter choice: ")    #sys.argv[1]
    choice = choice.lower()

    data = ["weight", "body fat %", "calories per day"]

    if choice == 'fill':
        for index, kind in enumerate(data,1):
            print(f"[{index}] - > {kind}")
        try:
            choice = int(input("Enter: "))
            mssg = data[choice-1]
            if choice == 3:
                print("Option not available right now.")
            
            else:
                week = int(input("Enter the week: "))
                print("[INFO] searching the week table...")
                try:
                    coord = match_table(week)
                    print("[INFO] Week table found succesfully.")
                    stuff = []
                    while True:
                        value = float(input(f"Enter the {mssg}: "))
                        stuff.append(value)
                        if len(stuff) == 7:
                            break
                    if choice == 1:
                        fill_in(coord[0] + 1, coord[1] + 1,stuff)
                    else:
                        fill_in(coord[0] + 1, coord[1] + 2,stuff)
                    print(f"[INFO] {mssg} data filled succesfully.")

                except:
                    print("[INFO] Something was wrong, table couldn' be found.")
        except ValueError:
            print("A number is expected.")
    
    elif choice == 'create':
        try:
            week = int(input("Enter the week number: "))
            try:
                prev_table_coord = match_table(week-1)
            except:
                print(f"[INFO] Week number wrong. Week {week-1} was not found.")
            new_coord = [prev_table_coord[0]+ 8 , prev_table_coord[1]]

            start_row = new_coord[0]
            start_col = new_coord[1]

            print("[INFO] Creating table...")
            table = body_weight_table(start_row, start_col, f"Week {week}")
            ss.batch_update(table.get_body())
            print("[INFO] The table was created succesfully.")

            initial_date = input("Enter the initial date (dd/mm/yyy): ")
            dates_to_fill = parse_date(initial_date)

            print("[INFO] Filling the dates...")
            fill_in(start_row+1, start_col, dates_to_fill)
            print("[INFO] Dates field filled succesfully.")            


        except ValueError:
            print("[INFO] Table couldn't be created, a number is expected.")
        except:
            print("[INFO] Something was wrong, table incompleted.")

    elif choice == 'check':
        try:
            coord = match_table(int(input("Enter the week number: ")))
            row = coord[0] +1
            col = coord[1] 
            date= worksheet.cell(row, col).value
            finish_day = parse_date(date, single_mode = True)
            prom_weight = worksheet.cell(row , col + 3).value
            print(f"The prom weight during the week {date}~{finish_day} is {prom_weight} kg")
        except ValueError:
            print("[INFO] A number is expected.")
    else:
        print("Work in progress :).")

main()
