import re
def introduction():
    #a) Check whether the given strings contain 0xB0. Display a boolean result as shown below.
    def ex1(string):
        regex = re.compile(r"0xB0")
        if regex.search(string):
            print("True")
            return
        print("False")

    #b) Replace all occurrences of 5 with five for the given string.
    def ex2(string):
        return re.sub(r"5","five", string)

    #c) Replace first occurrence of 5 with five for the given string.
    def ex3(string):
        return re.sub(r"5","five",string, count=1)

    #d) For the given list, filter all elements that do not contain e.
    def ex4(arg):
        if not isinstance(arg, list):
            raise Exception("A list is expected.")
        regex = re.compile(r"e")
        dissect = []
        for secuence in arg:
            if not regex.search(str(secuence)):
                dissect.append(secuence)
        
        return dissect

    #e) Replace all occurrences of note irrespective of case with X.
    def ex5(arg):
        match = re.sub(r"note", "X", arg, flags=re.IGNORECASE)
        return match

    #f) Check if at is present in the given byte input data.
    def ex6(arg):
        return bool(re.search(r"at", arg))
        
    #g) For the given input string, display all lines not containing start irrespective of case.
    def ex7(arg):
        lines = arg.split("\n")
        regex = re.compile(r"start", flags=re.IGNORECASE)
        target = []
        for line in lines:
            if not regex.search(line):
                target.append(line)
        return target

    #h) For the given list, filter all elements that contains either a or w.
    def ex8(arg):
        if not isinstance(arg, list):
            print("A list is expected")
            return
        regex = re.compile(r"a|w", flags=re.IGNORECASE)
        matches = []
        for element in arg:
            if regex.search(element):
                matches.append(element)
        return matches
    #i) For the given list, filter all elements that contains both e and n.
    def ex9(arg):
        if not isinstance(arg, list):
            print("A list is expected")
            return
        regex = re.compile(r"[en]",flags=re.IGNORECASE)
        matches = []
        for element in arg:
            if regex.search(element):
                matches.append(element)
        return matches
    #j) For the given string, replace 0xA0 with 0x7F and 0xC0 with 0x1F.
    def ex10(arg):
        mod1 = re.sub(r"0xA0","0x7F",arg)
        mod2 = re.sub(r"0xC0","0x1F",mod1)
        return mod2

def Anchors():
    #a) Check if the given strings start with be.
    def ex1(arg):
        regex = re.compile(r"^be")
        if regex.search(arg):
            print(f"{arg} starts with be.")


Anchors()