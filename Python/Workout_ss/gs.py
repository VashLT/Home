import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials


column_type = {
    1 : 'A',
    2 : 'B',
    3 : 'C',
    4 : 'D',
    5 : 'E',
    6 : 'F',
    7 : 'G',
    8 : 'H',
    9 : 'I',
    10: 'J',
    11: 'K',
    12: 'L',
    13: 'M',
    14: 'N',
}

def open_spread_sheet(ss_name):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(os.path.expanduser("~"),"jose2","Documents","workout.json"), scope)
    client = gspread.authorize(credentials)
    return client.open(ss_name)
