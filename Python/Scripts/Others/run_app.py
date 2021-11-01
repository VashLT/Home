import os
import sys

CHROME = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
FIREFOX = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"


def main(args):
    if len(args) > 1 and args[1].lower() == "firefox":
        browser = FIREFOX
        url = "/".join(["http://127.0.0.1:8000", *args[2:]])
        url += " -private"
    else:
        browser = CHROME
        url = "/".join(["http://127.0.0.1:8000", *args[1:]])
        url += " -incognito"
    print("runing")
    os.system(f"""
    "{browser}" {url}
    """)


if __name__ == "__main__":
    main(sys.argv)
