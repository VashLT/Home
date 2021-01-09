import json, os, sqlite3, logging, re, time, sys
import pyinputplus as pyip
from database import Database
from database import TABLE_NAME

from prettytable import PrettyTable
from datetime import datetime
from sqlite3 import Error
from pathlib import Path
from Modules.Screen.Screen import Screen

#! Python 3
#Family handler verison 0.1, realesed 07/06/2020 

"""
    This script keep track of my mom's cash, using sqlite to store data
"""
PATH = Path(Path.home()/'Home'/'Python'/'Scripts'/ 'tracker' /'register data')

#for debug purposes
if not os.path.exists(PATH):
    os.makedirs(PATH, exist_ok=True)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s',
handlers= [logging.FileHandler(filename = str(PATH/'debug.txt'), encoding= 'utf-8', mode = 'a+')])
# logging.disable(logging.CRITICAL)

class Logger():
    def __init__(self, cedula):
        """ arg is either money or a date """
        self.__id = cedula
        self.screen = Screen('Family handler', version = '0.1')
        self.db = Database('tracker.db')
        self.valid_user()
    
    def valid_user(self):
        self.screen.display()
        if not self.db.check(self.__id):
            try:
                print(f"[INFO] {self.__id} is not registered yet.", end=' ')
                ans = pyip.inputYesNo('Do you want to register? (y/n) ', limit =3, yesVal='y', noVal='n')
                if ans == 'y':
                    name = pyip.inputStr('Enter a name: ', limit=3)
                    money = pyip.inputInt('Initial money (default 0): ', limit =3, default=None)

                    response = self.db.register(self.__id, name, money)
                    if response:
                        self.add(money)                        
                        print(f'[INFO] User: (id:{self.__id}, name:{name}, money:{money}$) was succesfully registered in the Database.')
                    else:
                        print('[ERROR] Something was wrong with the register.')
                        print('Thanks for using the script!')
                        sys.exit()
                
                else:
                    sys.exit()
            except pyip.RetryLimitException:
                print(f'[ERROR] Limit of attempts exceeded.')
    
    def add(self, money):
        self.db.add_money(self.__id,money)

    def substract(self, money):
        self.db.add_money(self.__id, (-1)*money)

    def get_info(self, attribute):
        try:
            self.db.cursor.execute(
                f"""SELECT {attribute} FROM {TABLE_NAME} WHERE cc = {self.__id} """
            )
            response = self.db.cursor.fetchall()[0]
            logging.debug(f'Query: {attribute} and response: {response}')
            return response[0]
        except Exception as ex:
            print(f'[ERROR] Query failed. CAUSE: {ex}')
    
    def history(self, date = None):
        """ print history since a given date """
        logs = self.db.history[self.__id]
        start = 0 #index to start printing the transactions
        if date:
            print(f'[IN PROGRESS] Getting historial since {date} ...')
            logging.debug(f'given date {date}')
            start = get_start(logs, date)
            if not start: #means get_start return None
                print(f'[INFO] No dates match with {date}')
                start = 0 #set it as by default
        name = self.get_info('name')
        title = f'{name} - {self.__id} History'
        print(f"[IN PROGRESS] Building historial table ... ")
        self.history_table(logs[start:], title = title)
        input('') #wait to read the history
    
    def history_table(self,logs, title = 'History'):
        table = PrettyTable()
        table.title = title
        table.field_names = ['Total','Transaction', 'Message', 'Date', 'Hour']
        #fill in columns and rows
        for full_date, message, money, total in logs:
            date = full_date[:10]
            time = full_date[11:]
            table.add_row([total ,money, message, date, time])
        print(table)
            

def get_start(iterable, target_date):
    """ match if exists a given date and return its location """
    regex_date = re.compile(r'\d\d/\d\d/\d\d\d\d')
    for index,args in enumerate(iterable):
        full_date = args[0] #%d/%m/%Y %H:%M
        date = regex_date.search(full_date).group()
        if date == target_date:
            return index
    return None
                
    
        