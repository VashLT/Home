#!Python 3

# Database API

import sqlite3, json, os
from pathlib import Path
import pyinputplus as pyip
from datetime import datetime

TABLE_NAME = 'users'

class Database():
    def __init__(self, name):
        self.db = sqlite3.connect(name)
        self.cursor = self.db.cursor()
        self.init_db()
    
    def __del__(self):
        assert hasattr(self, 'history')
        #save file and database
        self.db.close()
        with open('history.json','w') as json_file:
            json.dump(self.history, json_file, indent=2, sort_keys=True )
    
    def check(self, cc):
        """ check existence of an user by their cc"""
        self.cursor.execute(f"""
            SELECT EXISTS( SELECT name FROM {TABLE_NAME} WHERE cc = {cc})
            """)
        response = self.cursor.fetchone()[0]
        # 1 exists, otherwise not exists
        if response == 1:
            return True
        else:
            return False    
    
    def init_db(self):
        #check whether db has users table or not      
        self.cursor.execute( f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} 
                (
                    cc integer PRIMARY KEY,
                    name text NOT NULL,
                    money integer DEFAULT 0
                )""")
        try:
        #init or open json file that store the history
            with open("history.json", encoding='utf-8') as json_file:
                self.history = json.load(json_file)
                
        except FileNotFoundError: #first creation of the file
            self.history = {}
        except Exception as ex:
            print(f"[ERROR] Couldn't open the history file - {ex}")
    
    def register(self, cc, name, money):
        try:
            self.cursor.execute( """INSERT INTO users (cc, name, money)
                    VALUES (?,?,?)
                """, (cc, name, money) )
            return True
        except Exception as ex:
            print(f'[ERROR] {ex}')
            return False
    
    def add_money(self,cc, money):
        """ add money and message """
        try:
            message = pyip.inputStr(prompt='Message (Mandatory): ', limit=3)
        except pyip.RetryLimitException:
            print('[INFO] Limit of attempts exceeded.')
            
        if money >= 0: verbs = ["Adding", "Added"]
        else: verbs = ["Substracting", "Substracted"]

        print(f'[IN PROGRESS] {verbs[0]} money ...')
        self.cursor.execute(
            f"""UPDATE {TABLE_NAME} SET money = money + {money} WHERE cc = {cc}""")
        self.update_history(cc,message, money)
        self.db.commit()
        print(f'[INFO] {verbs[1]} money succesfully.')
        total_money = self.query(cc, 'money')
        print(f"[INFO] TOTAL Money : ${total_money}")
    
    def query(self, cc, data):
        """ get attribute data in a row """
        try:
            self.cursor.execute(f"""
                SELECT {data} FROM {TABLE_NAME} WHERE cc = {cc}
            """)
            return self.cursor.fetchone()[0]
        except Exception as ex:
            print(f"[ERROR] Query failed. Unable to access {data} in cc: {cc}")
            return None
            
    def update_history(self,cc, reason, money):
        """ write history file with format: (date, message,  money) """
        self.history.setdefault(cc, []) #if there's no exist create it the key

        total = self.query(cc, 'money')
        date_format = r"%d/%m/%Y %H:%M"
        date = datetime.now().strftime(date_format)
        self.history[cc].append((date, reason, '$' + str(money), '$' + str(total) ))


