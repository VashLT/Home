# Python 3.7.4

# Database API
import sqlite3

import json

import os

from pathlib import Path

import pyinputplus as pyip

from datetime import datetime

from Modules.Debug.debugging import Logger

import traceback


STORAGE_PATH = os.path.join(os.getenv("HOME"),"Home", "Python", "Scripts", "PW", "data")
LOG_FILE_PATH = os.path.join(STORAGE_PATH, "debug.log")
HISTORY_FILE = os.path.join(STORAGE_PATH, "history.json")


class Database(sqlite3.Connection):
    def __init__(self, name):
        """
            DML: http://prntscr.com/w7f9hs

        """
        try:
            super().__init__(name)
        except sqlite3.OperationalError:
            super().__init__()
        self.log = Logger(path_log_file=LOG_FILE_PATH, level="debug")
        self.__cur = self.cursor()
        self.tables = {"users": ("user_id", "name", "register_date"),
                       "passwords": ("pw_id",
                                     "user_id",
                                     "pw_ref",
                                     "pw_hash",
                                     "register_date")}
        self.run_db()

    def __del__(self):
        assert hasattr(self, "history")
        # save file and database
        self.commit()
        self.close()
        with open(HISTORY_FILE, "w") as json_file:
            json.dump(self.history, json_file, indent=2, sort_keys=True)

    def check(self, user_id):
        """ check existence of an user by their id"""
        self.__cur.execute(f"""
            SELECT EXISTS( SELECT * FROM users WHERE user_id = {user_id})
            """)
        response = self.__cur.fetchone()[0]
        if response == 1:
            return True
        else:
            return False

    def _get_pw_id(self, **kwargs):
        """
            kwargs: {'attr_name': 'value', ...}
        """
        try:
            where_clause = ''
            for attr, value in kwargs.items():
                item = value
                if isinstance(value, str):
                    item = f"'{value}'"
                where_clause += f"{attr} = {item} AND "
            where_clause = where_clause[:-5]
            self.__cur.execute(f"""
                SELECT pw_id FROM passwords WHERE {where_clause};
            """)
            return self.__cur.fetchone()[0]
        except Exception:
            self.log.exception(traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def run_db(self):
        self.__cur.execute(f"""CREATE TABLE IF NOT EXISTS users(
                    user_id integer PRIMARY KEY, 
                    name VARCHAR(50),
                    register_date DATE);""")
        self.__cur.execute(f"""CREATE TABLE IF NOT EXISTS passwords(
                    pw_id integer PRIMARY KEY,
                    user_id integer,
                    pw_ref VARCHAR(100),
                    pw_hash VARCHAR(200),
                    register_date DATE,
                    FOREIGN KEY(user_id) REFERENCES users(user_id));
                    """)
        try:
            with open(HISTORY_FILE, encoding="utf-8") as json_file:
                self.history = json.load(json_file)

        except FileNotFoundError:  # first creation of the file
            self.history = {}
        except Exception as ex:
            self.log.exception(traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def exists(self, user_id):
        """ check existence of an user by their id"""
        self.__cur.execute(f"""
            SELECT EXISTS( SELECT name FROM users WHERE user_id = {user_id})
            """)
        response = self.__cur.fetchone()[0]
        # 1 exists, otherwise not exists
        if response == 1:
            return True
        else:
            return False

    def register_pw(self, pw_id, user_id, pw_ref, pw_hash):
        try:
            self.__cur.execute("""INSERT INTO passwords VALUES (?, ?, ?, ?, ?)
                """, (pw_id, user_id, pw_ref, pw_hash, Database.date(datetime.now())))
            self.update_passwords(pw_id, user_id, pw_hash, new=True)
            return True
        except Exception as ex:
            self.log.exception(
                f"TYPE: <{type(ex)}> - {ex}\n", traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")
            return False

    def register_user(self, user_id, name):
        try:
            self.__cur.execute("""INSERT INTO users (user_id, name, register_date)
                    VALUES (?, ?, ?)
                """, (user_id, name, Database.date(datetime.now())))
            self.commit()
            self.history.setdefault(str(user_id), {"Passwords": {}})
            self.update_history()
            return True
        except Exception as ex:
            self.log.exception(
                f"TYPE: <{type(ex)}> - {ex}\n", traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")
            return False

    def change_pw(self, user_id, prev_pw_hash, pw_hash, pw_ref=None):
        try:
            set_clause = f"pw_hash = '{pw_hash}'"
            if pw_ref:
                set_clause += f", pw_ref = '{pw_ref}'"
            pw_id = self._get_pw_id(user_id=user_id, pw_hash=prev_pw_hash)
            self.__cur.execute(f"""
                UPDATE passwords SET {set_clause}
                    WHERE pw_id = ? ;
                """, (pw_id,))
            self.update_passwords(pw_id, user_id, pw_hash)
            return True
        except Exception as ex:
            self.log.exception(
                f"TYPE: <{type(ex)}> - {ex}\n", traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")
            return False

    def query(self, table_name, target_attr, many=False, **kwargs):
        """ get id of register through an AND of kwargs
            kwargs struct: 
                {'attr': value, ...}
            target_attr: list or simple string
        """
        try:
            if isinstance(target_attr, str):
                target_attr = [target_attr,]

            if not all([x in self.tables[table_name] for x in target_attr]):
                print(f"[ALERT] {target_attr} is/are not a valid attribute.")
                return
            conditions = attrs = ""
            for attr in target_attr:
                attrs += f"{attr}, "
            attrs = attrs[:-2]
            for key, value in kwargs.items():
                item = value
                if isinstance(value, str):
                    item = f"'{value}'"
                conditions += f"{key} = {item} AND "
            conditions = conditions[:-5]
            self.__cur.execute(f""" 
                SELECT {attrs} FROM {table_name} WHERE {conditions};
            """)
            if many:
                return self.__cur.fetchall()
            else:
                return self.__cur.fetchone()

        except KeyError:
            print(f"[ERROR] {table_name} is not a valid table.")
        except Exception as ex:
            self.log.exception(
                f"TYPE: <{type(ex)}> - {ex}\n", traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def raw_query(self, query, args=None):
        """ 
            query: str
            args: tuple
        """
        try:
            if args:
                self.__cur.execute(query, args)
            else:
                self.__cur.execute(query)
            return self.__cur.fetchall()
        except sqlite3.OperationalError as ex:
            self.log.exception(f"""
            [ERROR] Syntax error in query: {query}
            - <{type(ex)}> {ex} 
            - Database->raw_query
            """, traceback_info=traceback.format_exc())

    def update_passwords(self, pw_id, user_id, pw_hash, new=False):
        """ update json file """
        assert self.history[str(user_id)]
        user_id = str(user_id)
        pw_id = str(pw_id)
        try:
            pw_dict = self.history[user_id]["Passwords"]
            if new:
                try:
                    pw_dict[pw_id] = [pw_hash, Database.date(datetime.now())]
                except:
                    print(
                        f"[ERROR] Password not in DB yet. Database->update_passwords")
                    return
            else:
                if not pw_id in pw_dict:
                    raise Exception("Password id not in passwords dictionary.")
                pw_dict[pw_id].extend([pw_hash, Database.date(datetime.now())])
            self.commit()
            self.update_history()
        except Exception as ex:
            self.log.exception(
                f"TYPE: <{type(ex)}> - {ex}\n", traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def update_history(self):
        with open(HISTORY_FILE, "w") as json_file:
            json.dump(self.history, json_file, indent=2, sort_keys=True)

    @staticmethod
    def date(date_obj, date_format=None):
        try:
            if not date_format:
                date_format = r"%d/%m/%Y %H:%M"
            return date_obj.strftime(date_format)
        except ValueError:
            return date_format.strftime(r"%d/%m/%Y %H:%M")
