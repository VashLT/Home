"""
    This script search for a file in Videos folder that matches the current date,
    will move it to DESTINITY_PATH and will rename the file according to the input name
"""
#INPUT file name
#OUTPUT String of location and state

import shutil, os, time, sys
import pyinputplus as pyip
from pathlib import Path

#! Python 3

def get_current_date(date_format = None):
    """ return current date
        default format: year-month-day
    """
    if not date_format:
        date_format = r'%Y-%m-%d'
    #check a correct date format was given
    try:
        date = time.strftime(date_format)
        return date
    except ValueError:
        print(f"[ERROR] Invalid format string")

PATH = Path(
    Path.home() / 'jose2'/'Videos'
    )
DESTINITY_PATH = Path(
    r"F:\Classes"
    )

class OBSmanager():
    def __init__(self,args,path = DESTINITY_PATH):
        self.path = path
        self.digest_args(args)
    
    def digest_args(self, args):
        """ make easier adding new features"""
        if 'all' in args:
            files = self.get_files(date = '2020-')
            self.move_all(files)
        else:
            date = get_current_date()
            target = self.get_files(date = date)[0]
            try:
                name = pyip.inputStr("Type new file name: ", limit = 3)
                self.move_file(target,name = name,date = date )

            except pyip.RetryLimitException:
                print("[ERROR] Number of attempts excedeed.")
                sys.exit()

        print(f"[INFO] File(s) moved succesfully.")
        


    def get_files(self, date = None):
        if not date:
            date = get_current_date()
        files = []
        for file in os.listdir(PATH):
            if file.startswith(date):
                files.append(file)
        return files        

    def move_all(self, files):
        print(f"[IN PROCRESS] Moving {len(files)}...")
        for file in files:
            self.move_file(file)
        
    
    def move_file(self, file,name = None, date = '', ext = "mp4"):
        """ move a given file to self.path"""
        file_path = str(Path(PATH) / file) #concatenate path and file name to get its full path
        if not name:
            name = file
        new_name = name + " " + date + "." + ext
        print(f"[IN PROCRESS] Moving {file_path} to {str(self.path / new_name)} ...")
        shutil.move(file_path, self.path / new_name)


if __name__ == "__main__":
    OBSmanager(sys.argv)    
