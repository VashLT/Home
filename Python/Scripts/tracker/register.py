import os, logging, re, sys
from typing import List
import pyinputplus as pyip
import platform
from database import Database

from prettytable import PrettyTable
from pathlib import Path

# from Modules.Screen.Screen import Screen

#! Python 3
# Family handler verison 0.2, realesed 26/10/2021

"""
    This script keep track of my mom's cash, using sqlite to store data
"""
OS = platform.system()

if OS == "Windows":
    PATH = Path(
        Path.home()
        / "Documents"
        / "Home"
        / "Python"
        / "Scripts"
        / "tracker"
        / "register data"
    )
else:
    PATH = Path(Path.home() / ".vashlt")


# for debug purposes
if not os.path.exists(PATH):
    os.makedirs(PATH, exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler(
            filename=str(PATH / "debug.txt"), encoding="utf-8", mode="a+"
        )
    ],
)
# logging.disable(logging.CRITICAL)


class Logger:
    def __init__(self, cedula: int):
        """arg is either money or a date"""
        self.__id = cedula
        # self.screen = Screen("Family handler", version="0.1")
        self.db = Database()
        self.valid_user()

    def valid_user(self):
        # self.screen.display()
        if not self.db.exists(self.__id):
            try:
                print(f"[INFO] {self.__id} is not registered yet.", end=" ")
                ans = pyip.inputYesNo(
                    "Do you want to register? (y/n) ", limit=3, yesVal="y", noVal="n"
                )
                if ans == "y":
                    name = pyip.inputStr("Enter a name: ", limit=3)
                    money = pyip.inputInt(
                        "Initial money (default 0): ", limit=3, default=None
                    )

                    response = self.db.register(self.__id, name, 0)
                    if response:
                        self.add(money)
                        print(
                            f"[INFO] User: (id:{self.__id}, name:{name}, money:{money}$) was succesfully registered in the Database."
                        )
                    else:
                        print("[ERROR] Something was wrong with the register.")
                        print("Thanks for using the script!")
                        sys.exit()

                else:
                    sys.exit()
            except pyip.RetryLimitException:
                print(f"[ERROR] Limit of attempts exceeded.")

    def add(self, money):
        self.db.add_money(self.__id, money)

    def substract(self, money):
        self.db.add_money(self.__id, (-1) * money)

    def get_user(self):
        return self.db.get_user(self.__id)

    def history(self, date: str = ""):
        """print history since a given date"""
        user = self.db.get_user(self.__id)
        transactions = user["transactions"]
        start = 0  # index to start printing the transactions

        if date:
            print(f"[IN PROGRESS] Getting historial since {date} ...")
            logging.debug(f"given date {date}")
            start = get_start(transactions, date)

        title = f'{user["name"]} - {self.__id} History'
        print(f"[IN PROGRESS] Building historial table ... ")
        self.history_table(transactions[start:], title=title)
        input("")  # wait to read the history

    def history_table(self, transactions: List[dict], title="History"):
        table = PrettyTable()
        table.title = title
        # table.field_names = ["Total", "Transaction", "Message", "Date", "Hour"]
        table.field_names = ["Total", "Transaction", "Message", "Date"]
        # fill in columns and rows
        for transaction in transactions:
            date = transaction["date"]
            # time = full_date[11:]
            # table.add_row([total, money, message, date, time])
            table.add_row(
                [
                    transaction["total"],
                    transaction["amount"],
                    transaction["message"],
                    date,
                ]
            )

        print(table)


def get_start(iterable: list, target_date: str) -> int:
    """match if exists a given date and return its location"""
    regex_date = re.compile(r"\d\d/\d\d/\d\d\d\d")
    for index, transaction in enumerate(iterable):
        full_date = transaction["date"]  #%d/%m/%Y %H:%M
        print(full_date, type(full_date))
        date = regex_date.search(full_date).group()
        if date == target_date:
            return index

    return 0
