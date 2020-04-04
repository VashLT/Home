import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_formatting
import re
import batch_class
import gs
import google_ss_color
# pylint: disable=maybe-no-member
# pylint: disable=no-value-for-parameter
# pylint: disable=too-many-function-args
SPREADSHEET_NAME = "Workout"
SHEET_NAME = "Marzo"

def get_spreadsheet_id_from_url(url):
    id_regex = re.compile(r'/spreadsheets/d/([a-zA-Z0-9-_]+)')
    sheet_id = id_regex.findall(url)
    return sheet_id[0]

def body_weight_table(spreadsheet,sheet,start_row,start_col):
    palette_colors = ['LIGHT YELLOW 3','LIGHT RED 3','LIGHT ORANGE 3','LIGHT PURPLE 2','LIGHT RED BERRY 3']
    #table dimentions
    s_row = start_row
    e_row = start_row+8
    s_col = start_col
    e_col = start_col+4

    #create an instance of batch_dealing class
    table = batch_class.batch_dealing(sheet._properties['sheetId'])
    
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
    sheet.update_cell(s_row+1, e_col-1,f'=PROMEDIO({col}{s_row+1}:{col}{e_row-1})')

    title = 'Week 5'
    sheet.update_cell(s_row,s_col,title)
    table.font_size(10, s_row, s_col, bold = True)
    table.set_borders_range((0,0,0), "SOLID", s_row,s_row,s_col,e_col)
    table.set_color( google_ss_color.rgb('LIGHT CORNFLOWER 2'), s_row, s_col)
    #setting the alignment
    table.alignment_range("CENTER",s_row, e_row,s_col, e_col)

    return  table
    

def main():

    ss = gs.create_spread_sheet(SPREADSHEET_NAME)

    worksheet = ss.worksheet(SHEET_NAME)

    table = body_weight_table(ss, worksheet,38,2)
    #table = batch_class.batch_dealing(worksheet._properties['sheetId'])
    #table.set_borders((0,0,0), "SOLID", 38,1)

    response = ss.batch_update(table.get_body())


if __name__ == '__main__':
    main()