import shelve
import pyperclip
import os
import sys
import re

#! Python 3.8
# Multi-Clipboard manager v1.0
"""
this script store the data copied in the clipboard, implements the shelve
module to store it in a dict-like file, every key of the dict is given by
the user.
        """

PATH = os.path.join(os.path.expanduser("~"), "Documents",
                    "Home", "Python", "Scripts", "mcb data")
FILE_NAME = "Multi_Clip_Board"


class MultiClipBoard():
    def __init__(self, args):
        try:
            self.digest_arg(args)
        except Exception as ex:
            print(f"{type(ex)}")

    def digest_arg(self, args):
        length = len(args)
        if length < 2:  # prints the usage of the script
            usage = """
            Usage: mcb save (keyword): Save the current data stored in the clipboard with the keyword as key
                   mcb list          : Copy all the keywords to the clipboard
                   mcb (keyword)     : Copy the text stored to the clipboard if the given keyword exists

            """
            print(usage)

        else:
            try:
                with shelve.open(os.path.join(PATH, FILE_NAME)) as file:
                    if "save" in args:
                        # store the data in the clipboard according to the given keyword
                        data = pyperclip.paste()
                        keyword = " ".join(args[2:])
                        if not self.layer(keyword):
                            raise Exception("[ERROR] Keyword is expected.")
                        file[keyword] = data
                    elif "list" in args:  # copy to the clipboard all the stored keywords in an array
                        keywords = str(list(file.keys()))
                        pyperclip.copy(keywords)
                        print(keywords)
                    else:  # copy the stored data
                        keyword = " ".join(args[1:])
                        data = str(file[keyword])
                        pyperclip.copy(data)
            except Exception as ex:
                print(f"{type(ex)}")

    def layer(self, string):  # make sure to store keywords with no *-_%$#@!~``""... characters
        regex = re.compile(r"[^a-zA-Z0-9 ]")
        # if match any of these characters in the given string return False
        if regex.findall(string):
            return False
        return True


if __name__ == "__main__":
    MultiClipBoard(sys.argv)
