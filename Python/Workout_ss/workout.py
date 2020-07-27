from oauth2client.service_account import ServiceAccountCredentials
from datetime import timedelta, datetime
from prettytable import PrettyTable

import sys, os, re, gspread, time
import google_ss_color,gs, gspread_formatting,table #custom modules
import pyinputplus as pyip


#! Python3

# Workout spreadsheet manager 

# pylint: disable=maybe-no-member
# pylint: disable=no-value-for-parameter
# pylint: disable=too-many-function-args

SPREADSHEET_NAME = "Workout"
DEFAULT_ROW = 6
DEFAULT_COLUMN = 2


class Workout():
    def __init__(self):
        self.spreadsheet = gs.open_spread_sheet(SPREADSHEET_NAME)
        self.sheets = [sheet.title for sheet in self.spreadsheet.worksheets()]
        #Screen object to keep updating the main frame which shows the name of the script
        self.options = ["fill", "add", "create", "check","table"]
        self.fields = {"Date": 0,"Weight": 1,r"% fat" : 2, "Prom Weight" : 3, "Calories p/w" : 4} # {field : relative column taking origin from column 1}

    def set_worksheet(self, name):
        self.worksheet = self.spreadsheet.worksheet(name)
        self.update_formatter()

    def update_formatter(self):
        self.batch = table.BatchFormatter(self.worksheet._properties['sheetId'])

    def show_sheets(self):
        for index,sheet in enumerate(self.sheets,1):
            print(f"[{index}] {sheet}")

    def create_sheet(self, name):
        try:
            self.spreadsheet.add_worksheet(title = name, rows = "100", cols = "25")
            self.sheets.append(name)
        except Exception as ex:
            print(f"[ERROR] {type(ex)} - {ex}")


    def get_previous_table_coord(self):
        coord = None
        limit = 4 #max 4 weight tables per sheet
        #search for the previous table, max number of weeks per month is 4
        for week in range(limit, 0, -1):
            coord = self.find_table(week = week)
            if coord:
                return (coord, week)
        return None
    
    def update_location(self):
        self.location = self.find_table(week = self.week)
        assert self.location

    def create_table(self, title, row  = DEFAULT_ROW,col = DEFAULT_COLUMN,new = False):
        assert hasattr(self, "worksheet")
        print("[IN PROGRESS] Creating the weight table...")
        weight_table = table.Table(self.worksheet, row, col, title).format

        self.spreadsheet.batch_update(weight_table.get_body())
        
        if new: #for a just created sheet it's necessary a initial date
            initial_date = input("Enter the initial date (dd/mm/yyy): ")
        
        else:
            form = r"%d/%m/%Y" #DD/MM/YY
            raw_date = datetime.strptime(self.worksheet.cell(row - 1,col).value,form) + timedelta(days = 1) #search for the corresponding initial day in the previous body weight table
            initial_date = raw_date.strftime(form)

        dates_to_fill = self.construct_dates(initial_date)

        print("[IN PROGRESS] Filling the dates...")
        self.fill_data(row+1, col, dates_to_fill)
        print("[INFO] Dates filled succesfully.")
        #update the current working week
        self.week = [int(char) for char in title if char.isdigit()][0]
        print("[INFO] The weight table was created succesfully.")
        self.update_location()
    
    def find_table(self, week):
        try:
            cell_match = self.worksheet.find("Week %s" % str(week))
            location = (cell_match.row , cell_match.col) #coords (x,y)
            return location
        except gspread.CellNotFound:
            return None


    def construct_table(self):
        values = self.get_data()
        table = PrettyTable()
        table.title = "Week %s" % self.week
        table.field_names = self.fields
        #construct table
        index = 1
        for date, weight, fat in values[0]:
            if index == 4:
                table.add_row([date, weight, fat, values[1], values[2]])
            else:
                table.add_row([date, weight, fat,'', ''])
            index += 1
        
        return table
    
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
                return False
                
            cell = self.worksheet.cell(row + cont,column)
        self.worksheet.update_cell(cell.row, cell.col, value)
        return True

    def merge(self,row,col):
        self.batch.merge_cells(row,row+6,col,col)
        self.spreadsheet.batch_update(self.batch.get_body())

    def get_data(self):
        """ get all data store in the current week number"""
        try:
            init_row, init_col = self.find_table(self.week)
            init_row += 1
            data = []
            #find dates, weights and %fat 
            for row in range(init_row, init_row + 7):
                date = self.worksheet.cell(row, init_col).value     
                weight = self.worksheet.cell(row, init_col + 1).value
                fat = self.worksheet.cell(row, init_col + 2).value
                data.append((date, weight, fat))

            prom_weight = self.worksheet.cell(init_row, init_col + 3).value
            calories = self.worksheet.cell(init_row, init_col + 4).value

            return [data, prom_weight, calories]

        except Exception as ex:
            print(f"[ERROR] {ex}")
            return None

