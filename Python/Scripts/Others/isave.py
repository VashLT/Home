import pyinputplus as pyip
import re
import os
from PIL import ImageGrab
DEFAULT_PATH = os.path.join(os.getenv("HOME"), "Pictures")


def main():
    try:
        print(f"Default path: {DEFAULT_PATH}")
        im = ImageGrab.grabclipboard()
        path = input("Enter path: ")
        tries = 0
        while not os.path.exists(path):
            if path == '':
                path = DEFAULT_PATH
                break
            print(f"{path} is not a valid path. ")
            tries += 1
            path = input("Enter path: ")
            if tries > 3:
                raise Exception("Excedeed number of tries")
        name = re.sub(r"\.+", "", input("Enter image name: "))
        print(f"[IN PROGRESS] Saving image ...")
        im.save(os.path.join(path, name + ".png"), "PNG")
        print(f"[INFO] Image succesfully saved at {os.path.join(path, name+'.png')}")
        
    except Exception as ex:
        print(f"[ERROR] Something went wrong. {ex}")


if __name__ == "__main__":
    main()
