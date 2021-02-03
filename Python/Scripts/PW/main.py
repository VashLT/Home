from controller import Controller
from utils import Utils
from Modules.Screen.Screen import Screen
import traceback
import sys, os
from time import sleep
from Modules.Debug.debugging import Logger


# TODO: parse pw_ref with spaces
STORAGE_PATH = os.path.join(os.getenv("HOME"),"Home", "Python", "Scripts", "PW", "data")
LOG_FILE_PATH = os.path.join(STORAGE_PATH, "interface_debug.log")


class Interface(object):
    def __init__(self, *args):
        self.log = Logger(path_log_file=LOG_FILE_PATH, level = "warning")
        self.sc = Screen("PW manager")
        self.sc.display()
        sleep(2)
        self.digest_args(*args)

    def __del__(self):
        print(f"[IN PROGRESS] Exciting ...")

    @staticmethod
    def usage():
        print(f"""
            Usage:
                -> $pw --list | -l: List all the store password references
                -> $pw --save | -s [password | -cb]: If not password as argument, then store clipboard data as a pw and prompt for a password reference.
                -> $pw --change | -c [pw_ref]: if not pw_ref, then user is prompted for the reference as well as the new password
                -> $pw pw_ref: Verify user and copy pw to clipboard if matches, otherwise will prompt to select the underlying pw_ref based on better
                matches to the input ref.
        """)

    def digest_args(self, *args):
        try:
            self.sc.display()
            if not args:
                Interface.usage()
                return
            self.ctrl = Controller(screen=self.sc)
            if not self.ctrl.has_user():
                return
            index = 0
            while index < len(args):
                self.sc.display()
                arg = args[index]
                self.log.info(f"Reading arg {arg}")
                if arg and not "-" in arg:
                    self.log.info(f"Calling search_pw") 
                    self.ctrl.search_pw(arg)
                elif arg == "--list" or arg == "-l":
                    self.log.info(f"Calling list_pws") 
                    self.ctrl.list_pws()
                elif arg == "--save" or arg == "-s":
                    cfc = "--clipboard" in args or "-cb" in args
                    self.ctrl.save_pw(pw= Utils.check_next_arg(args, index), copy_from_clipboard=cfc)
                    index += 1
                elif arg == "--change" or arg == "-c":
                    self.ctrl.change_pw(pw=Utils.check_next_arg(args, index))
                sleep(2)
                index += 1

        except Exception as ex:
            traceback.print_exc(file=sys.stdout)


if __name__ == "__main__":
    Interface(*sys.argv[1:])
