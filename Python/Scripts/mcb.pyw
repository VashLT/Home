import shelve, pyperclip, os, sys, re

#! Python 3
# Multi-Clipboard manager v1.0
"""
this script store the data copied in the clipboard, implements the shelve
module to store it in a dict-like file, every key of the dict is given by
the user.
        """

PATH = os.path.join(os.path.expanduser("~"),"jose2","Documents","Home","Python","Scripts","mcb data")
FILE_NAME = "Multi_Clip_Board"

class MultiClipBoard():
    def __init__(self, *args):
        try:
            self.digest_arg(*args)
        except Exception as ex:
            print(f"{type(ex)}")
    

    def digest_arg(self, *args):
        length = len(args)
        if length < 2: #prints the usage of the script
            usage = """
            Usage: mcb save (keyword): Save the current data stored in the clipboard with the keyword as key
                   mcb list          : Copy all the keywords to the clipboard
                   mcb (keyword)     : Copy the text stored to the clipboard if the given keyword exists

            """
            print(usage)
        
        else:
            try:
                with shelve.open(os.path.join(PATH, FILE_NAME)) as file:
                    if args[1] == "save":
                        #store the data in the clipboard according to the given keyword
                        data = pyperclip.paste()
                        keyword = " ".join(args[2:])
                        if not self.layer(keyword):
                            raise Exception("[ERROR] Keyword is expected.")
                        file[keyword] = data
                    elif args[1] == "list": #copy to the clipboard all the stored keywords in an array
                        keywords = str(list(file.keys()))
                        pyperclip.copy(keywords)
                    else: #copy the stored data
                        keyword = " ".join(args[1:])
                        data = str(file[keyword])                 
                        pyperclip.copy(data)
            except Exception as ex: 
                print(f"{type(ex)}")
    
    def layer(self, string): #make sure to store keywords with no *-_%$#@!~``""... characters
        regex =re.compile(r"[^a-zA-Z0-9 ]")
        if regex.findall(string): #if match any of these characters in the given string return False
            return False
        return True
                    
        
if __name__ == "__main__":
    MultiClipBoard(*sys.argv)

