import sys

import os


def args_to_command(*args):
    command = ""
    N = len(args)
    for index, arg in enumerate(args):
        if arg == "-s" or arg == "--save":
            if index + 1 < N and args[index + 1].startswith("-"):
                continue
            command += "/p %s" % args[index + 1]
        elif arg == "-n" or arg == "--name":
            if index + 1 < N and args[index + 1].startswith("-"):
                continue
            command += "/f %s" % args[index + 1]
    return command


def main(*args):
    com_args = args_to_command(*args)
    cli = "IDMan "


if __name__ == "__main__":
    main(*sys.argv)
