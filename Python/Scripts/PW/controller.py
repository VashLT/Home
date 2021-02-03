#! Python 3.7.4

"""
This file contains the controller class which takes care of main tasks such as hashing
passwords, getting users from the db, and so on.
        """

import shelve

import random

import pyperclip

import os

import sys

import re

import pyinputplus as pyip

from db import Database

from utils import Utils

from Modules.Debug.debugging import Logger

import traceback


# Controller class

DATA_PATH = os.path.join(os.getenv("HOME"), "Home", "Python", "Scripts", "PW", "data")
LOG_FILE_PATH = os.path.join(DATA_PATH, "debug.log")


class ControllerException(Exception):
    """
        Base class for exceptions
    """
    pass


class NotRegisterUserException(ControllerException):
    """
        This exception is raised when the user is asked for
        register but input 'no'.
    """
    pass


class InputException(ControllerException):
    """
        This exception is raised whenever the user go wrong
        in an input state
    """
    pass


class ImpossibleExepction(ControllerException):
    """
        This exception is raised in weird cases.
    """
    pass

class Controller(object):
    def __init__(self, screen):
        self.log = Logger(path_log_file=LOG_FILE_PATH)
        self.sc = screen
        self.db = Database(os.path.join(DATA_PATH, "data.db"))
        try:
            self.__users = shelve.open(os.path.join(DATA_PATH, "data"))
        except Exception as ex:
            print(f"{type(ex)}")

        self._get_user()

    def __del__(self):
        self.__users.close()

    def _get_user(self):
        try:
            while True:
                self.sc.display()
                user = input(f"[INPUT] Enter username: (If new user press Enter to register)\n")
                if user == '':
                    self._register_user()
                    continue
                pin = Utils.input_pin(prompt="[INPUT] Enter PIN: \n", length = 4, attempts = 3)
                if user in self.__users:
                    if self.check_user(user, pin):
                        self.__username = user
                        break
                    print(f"[INFO] Given username and PIN doesn't match. Please try again ...")
                else:
                    print(f"[INFO] Ups. We have detected you are not a user yet.")
                    ans = pyip.inputYesNo(f"[INPUT] Do you want to register? (y/n)\n", yesVal='y', noVal='n', limit=3)
                    if ans != 'y':
                        raise NotRegisterUserException()
                    self._register_user()
            self.__user_id = self.__users[self.__username][1]
        
        except pyip.RetryLimitException:
            print(f"[ERROR] Excedeed limit of attempts")
        except NotRegisterUserException:
            return
        except Exception as ex:
            self.log.exception( f"TYPE: <{type(ex)}> - {ex}\n" , traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def _get_user_pw(self, attrs):
        """ 
           return data as a list of tuples like [(attr1, attr2, ...), (... , ...)] 
        """
        assert hasattr(self, f"_{type(self).__name__}__user_id")
        try:
            return self.db.query(
                "passwords", attrs, many = True,user_id = self.__user_id)
            
        except Exception as ex:
            self.log.exception( f"TYPE: <{type(ex)}> - {ex}\n" , traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def _get_user_data(self, attrs):
        """
            attrs: list
            output: tuple
        """
        try:
            return self.db.query(
                "users", attrs, user_id = self.__user_id
            )
        except Exception as ex:
            self.log.exception( f"TYPE: <{type(ex)}> - {ex}\n" , traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def _get_pw(self, pw_ref, hashed = False):
        assert hasattr(self, f"_{type(self).__name__}__user_id")
        try:
            encrypted_pw = self.db.query(
                "passwords", "pw_hash", user_id = self.__user_id, pw_ref = pw_ref
            )[0]
            if hashed:
                return encrypted_pw
            else:
                return Utils.decrypt(encrypted_pw)
        except Exception as ex:
            self.log.exception( f"TYPE: <{type(ex)}> - {ex}\n" , traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def _change_user(self):
        try:
            while True:
                user = pyip.inputStr(f"[INPUT] Enter username: \n", limit=3)
                pin = pyip.inputStr(f"[INPUT] Enter user PIN: \n", limit=3)
                if self.check_user(user, pin):
                    break
                print(f"[INFO] Username or PIN are wrong.")
            self.__user_id = self.__users[user][1]
        except pyip.RetryLimitException:
            raise InputException()
        except Exception as ex:
            self.log.exception( f"TYPE: <{type(ex)}> - {ex}\n" , traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def has_user(self):
        if hasattr(self, f"_{type(self).__name__}__user_id"):
            return True
        else:
            return False

    def get_users(self):
        try:
            return list(self.__users.keys())
        except Exception as ex:
            self.log.exception( f"TYPE: <{type(ex)}> - {ex}\n" , traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    #pylint: disable=no-self-argument
    def store_user(register):
        def storage_handling(self):
            try:
                assert hasattr(self, "db")
                self.sc.display()
                print("[IN PROGRESS] Register process ...")
                #pylint: disable=not-callable
                user, pin = register(self)
                user_id = self.generate_id()
                self.db.register_user(user_id, user)  # sqlite3 manage
                self.__users[user] = (pin, user_id)  # shelve manage
                self.__username = user
            except Exception:
                self.log.exception(traceback.format_exc())
                print(
                    f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")
        return storage_handling

    @store_user
    def _register_user(self):
        """ prompt user for username and pin"""
        user = Utils.input_user(self, prompt = f"[INPUT] Enter username: \n", attempts=3, max_len = 32)
        while True:
            pin = Utils.input_pin(f"[INPUT] Enter user PIN: \n")
            re_pin = Utils.input_pin(f"[INPUT] Confirm your PIN: \n")
            if pin == re_pin:
                return (user, pin)
            print(f"[INFO] PINs don't match. Please try again ...")

    def list_pws(self):
        try:
            data = self._get_user_pw(["pw_ref", "register_date"])
            username = self._get_user_data(["name"])[0]
            if not data:
                print(f"[INFO] {username} has no passwords registered yet.")
                return
            table = Utils.build_table(
                columns=["PW ref name", "Register date"],
                title=f"{username} Passwords",
                data=data,
                date_index= 1
            )
            print(table)
        except Exception as ex:
            self.log.exception( f"TYPE: <{type(ex)}> - {ex}\n" , traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def _search_ref(self, arg):
        """
            > Search password reference by a sub string and return the exact ref or prompt for a choice among a list of references
            arg: str
            output: query result
        """
        try:
            data = self.db.raw_query(f"""
                SELECT pw_ref FROM passwords WHERE user_id = ? AND LOWER(pw_ref) LIKE '%{arg.lower()}%';
            """, (self.__user_id,))
            if not data:
                print(f"[INFO] No reference pw names matched to {arg}.")
                return
            else:
                if len(data) == 1:
                    pw_ref = data[0][0]
                else:
                    print(f"[LIST] Similar references that matched {arg}")
                    [print(f"\t[{index}] {ref[0]}")
                     for index, ref in enumerate(data, 1)]
                    opt = pyip.inputInt(
                        f"[INPUT] Reference number: ", max=len(data), min=1, limit=3)
                    pw_ref = data[opt - 1][0]
            return pw_ref
            
        except Exception as ex:
            self.log.exception(
                f"TYPE: <{type(ex)}> - {ex}\n", traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def search_pw(self, arg):
        """
            arg: str
            output: password or None
        """
        try:
            pw_ref = self._search_ref(arg)
            print(
                f"[IN PROGRESS] Copying to clipboard pw associated with {pw_ref} ...")
            pyperclip.copy(self._get_pw(pw_ref))
            print(f"[INFO] Password succesfully copied!.")
        except Exception as ex:
            self.log.exception( f"TYPE: <{type(ex)}> - {ex}\n" , traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def save_pw(self, pw=None, copy_from_clipboard=True):
        try:
            if not pw and copy_from_clipboard:
                print("[IN PROGRESS] Copying password from clipboard ...")
                pw = pyperclip.paste()
                if pw == '':
                    print("[ALERT] No password was found in clipboard.")
                    ans = pyip.inputYesNo("Do you want to input the password? (y/n): \n", yesVal='y', noVal='n')
                    if ans != 'y':
                        print("[INFO] No passwords were saved.")
                        return
                    pw = Utils.input_pw()
            elif not pw:
                pw = Utils.input_pw()
            pw_ref = Utils.input_ref(max_len=32)
            print("[IN PROGRESS] Storing password ...")
            pw_id = Utils.autoincrement_id(self.db, table_name="passwords")
            if not self.db.register_pw(pw_id, self.__user_id, pw_ref, pw_hash=Utils.encrypt(pw, encoding='utf-8')):
                print(f"[INFO] No passwords were saved.")
                return
            print(f"[INFO] Password succesfully stored!")
        except Exception as ex:
            self.log.exception( f"TYPE: <{type(ex)}> - {ex}\n" , traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")
    
    #TODO: decide whether password can be change just by user credentials and ref, or if it's necessary input the old password
    def change_pw(self, ref=None, pw=None):
        try:
            while True:
                if not ref:
                    ref = Utils.input_ref(
                        prompt="[INPUT] Enter a password reference to the password: \n",
                        max_len=32)
                pw_ref = self._search_ref(ref)
                if not pw_ref:
                    print(f"[INFO] The following is the {self.__username}'s list of references")
                    self.list_pws()
                    ref = None
                else:
                    break
            if not pw:
                [print(f"[{index}] {opt}") for index, opt in enumerate(["Copy from clipboard", "Input password"], 1)]
                opt = pyip.inputInt(f"[INPUT] Option: ", max=2, min=1, limit=3)
                if opt == 1:
                    print("[IN PROGRESS] Copying password from clipboard ...")
                    pw = pyperclip.paste()
                    if pw == '':
                        print("[ALERT] No password was found in clipboard.")
                        ans = pyip.inputYesNo(
                            "Do you want to input the password? (y/n): \n", yesVal='y', noVal='n')
                        if ans != 'y':
                            print("[INFO] No passwords were saved.")
                            return
                        pw = Utils.input_pw(prompt="[INPUT] Enter the new password: \n")
                elif opt == 2:
                    pw = Utils.input_pw(
                        prompt="[INPUT] Enter the new password: \n")
            print("[IN PROGRESS] Storing password ...")
            if not self.db.change_pw(self.__user_id,
                                    self._get_pw(pw_ref, hashed=True),
                                    Utils.encrypt(pw)):
                print(f"[INFO] No passwords were saved.")
                return
            print(f"[INFO] Password succesfully stored!")
            
        except Exception as ex:
            self.log.exception(
                f"TYPE: <{type(ex)}> - {ex}\n", traceback.format_exc())
            print(
                f"[ERROR] An exception has ocurred. check {LOG_FILE_PATH} for more info.")

    def generate_id(self):
        top = 1e6
        it = 1
        while True or it < top:
            pos_id = random.randint(1, top)
            if not self.db.exists(pos_id):
                return pos_id
            it += 1
        raise ImpossibleExepction()

    def check_user(self, user, pin):
        if not user in self.__users or pin != self.__users[user][0]:
            return False
        return True

        
