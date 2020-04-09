import pyperclip
import sys
import os
import time
from Display_Screen.Screen import Screen

#! Python 3
# A char counter program 

special_chars = ["\n","\t","\b","\f","\a","\r"]

def char_counter(message, blanks = True):
    chars = {}
    for char in message:
        if not blanks:
            if char == " ":
                continue
        if char in special_chars:
            raw = char.encode('unicode_escape')
            parse = raw.decode('utf-8')
            chars.setdefault(parse, 0)
            chars[parse] += 1
            continue
        chars.setdefault(char, 0)
        chars[char] += 1
    return chars


screen = Screen('Char Counter')
screen.display()
if len(sys.argv) < 2:
    print("Usage: (char 1) print the number of times a character appear")
    print("       (char 2) print the number of times a character appear (without blanks)")
    print("       (char 3) print only the length")
    sys.exit()

arg = sys.argv[1]
try:
    arg = int(arg)
    blanks = True
    string = pyperclip.paste().replace(' ','')
    if arg == 3:
        print(f"There are {len(string)} words.")
        sys.exit()
    elif arg == 1:
        print(f"There are {len(pyperclip.paste())} words.")
    elif arg == 2:
        print(f"There are {len(string)} words.")
        blanks = False
    chars = char_counter(str(pyperclip.paste()), blanks)
    for char in chars.keys():
        print(f"[{char}] : {chars[char]}")

except ValueError:
    print("The second argument must be a number")


