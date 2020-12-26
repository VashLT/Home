from PIL import ImageGrab
import re
import os

def save_image_from_clipboard(path_to_save, name):
    try:
        im = ImageGrab.grabclipboard()
        name = re.sub(r"\.+", "", name)
        if not os.path.exists(path_to_save):
            raise Exception(f"{path_to_save} doesn't exist.")
        path = os.path.join(path_to_save, name + ".png")
        im.save(path, "PNG")
        return path
    except Exception as ex:
        print(f"[ERROR] Problem when saving image from clipboard. {ex}")
