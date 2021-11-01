from cryptography.fernet import Fernet
from getpass import getpass
from prettytable import PrettyTable
from datetime import datetime
import re
import os


def check_chars(string, regex=None):
    if not regex:
        regex = r"[^a-zA-Z0-9]"
    regex = re.compile(regex)
    if regex.findall(string):
        return False
    return True


def is_integer(num):
    try:
        return float(num) == int(num)
    except ValueError:
        return False


def is_date(string, regex=None):
    if not regex:
        regex = r"\d{2,4}(- | /)\d{2,4}(- | /)\d{2,4}"
    re_date = re.compile(regex, re.VERBOSE)
    if re_date.findall(string):
        return True
    return False


class Utils(object):
    @staticmethod
    def autoincrement_id(db_obj, table_name):
        total = int(db_obj.raw_query(f"""
           SELECT COUNT(*) FROM  {table_name}
        """)[0][0])
        return total + 1

    @staticmethod
    def input_ref(prompt=None, attempts=3, max_len=32):
        if not prompt:
            prompt = "[INPUT] Enter a reference name to the password: \n"
        it = 0
        while True:
            ref = input(prompt)
            if len(ref) > max_len:
                print(
                    f"[INFO] reference must be less than {max_len + 1} character length. ")
            elif ref == '':
                print(f"""[INFO] ref can't be empty. """)
            else:
                return ref
            it += 1
            if it > attempts:
                raise Exception(f"Excedeed input attempts")

    @staticmethod
    def input_user(obj, prompt=None, attempts=3, max_len=32, regex=None):
        if not prompt:
            prompt = "[INPUT] Enter username: \n"
        it = 0
        while True:
            user = input(prompt)
            if len(user) > max_len:
                print(
                    f"[INFO] username must be less than {max_len + 1} character length. ")
            elif not check_chars(user, regex=regex):
                print(
                    f"""[INFO] username can't contain chars like *-_%$#@!~``""...""")
            elif user in obj.get_users():
                print(f"""[INFO] {user} already exists.""")
            else:
                return user
            it += 1
            if it > attempts:
                raise Exception(f"Excedeed input attempts")

    @staticmethod
    def input_pin(prompt=None, attempts=3, length=4):
        if not prompt:
            prompt = "[INFO] Enter PIN: \n"
        it = 0
        while True:
            pin = getpass(prompt=prompt)
            if len(pin) != length:
                print(f"[INFO] PIN must be {length} digits length. ")
            elif not is_integer(pin):
                print(f"[INFO] PIN must be an integer")
            else:
                return pin

            it += 1
            if it > attempts:
                raise Exception(f"Excedeed input attempts")

    @staticmethod
    def input_pw(prompt=None, attempts=3, max_len=32):
        if not prompt:
            prompt = "[INFO] Enter Password: \n"
        it = 0
        while True:
            pw = getpass(prompt=prompt)
            if len(pw) > max_len:
                print(
                    f"[INFO] Password must be less than {max_len} characters length. ")
            else:
                return pw
            it += 1
            if it > attempts:
                raise Exception(f"Excedeed input attempts")

    @staticmethod
    def encrypt(password, encoding='utf-8'):
        """
            password: str
            output: password encrypted
        """
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        ciphered_pw = cipher_suite.encrypt(bytes(password.encode(encoding)))
        hash_pw = key + ciphered_pw
        return hash_pw.decode(encoding)

    @staticmethod
    def decrypt(encrypted_pw, encoding="utf-8"):
        if not isinstance(encrypted_pw, bytes):
            encrypted_pw = encrypted_pw.encode(encoding)
        key = encrypted_pw[:44]
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(encrypted_pw[44:]).decode(encoding)

    @staticmethod
    def check_next_arg(args, index):
        """
            args: list
            index: int
            output: str or None
        """
        if len(args) <= index + 1 or not args[index + 1] or "-" in args[index + 1]:
            return
        else:
            return args[index + 1]
        

    @staticmethod
    def format_date(date_str, old_fmt, new_fmt=r"%d-%m-%Y %H:%M %p"):
        return datetime.strptime(date_str, old_fmt).strftime(new_fmt)

    @staticmethod
    def build_table(columns, title, data, date_index=None, prev_date_fmt=r"%d/%m/%Y %H:%M"):
        """
            columns: list
            title: str
            data: tuple or list
            output: table
        """
        table = PrettyTable()
        table.title = title
        table.field_names = columns
        [table.add_row(row) for row in data]
        return table

