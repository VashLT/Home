#!python3
import datetime
import pyperclip
import cv2
import sys
import pyautogui
import os
import info
import time
import numpy as np
import pyinputplus as pyip
from Modules.Screen.Screen import Screen
import playsound
import threading
import pause
from wspp import WhatsApp
# copy image to clipboard
from io import BytesIO
import win32clipboard
from PIL import Image


TUTOR_NAME = "José Silva"
SHIFT_TIME = 2
TIME_DELAY = 40
# pages
CHAT_LINK = "https://chat.google.com/u/1/room/AAAA-GynUA0"
SPREADSHEET_LINK = "https://docs.google.com/spreadsheets/u/1/d/1QGVpyCU8GcHngoPVwljOm3TXJsUSFCoF/edit?usp=drive_web&ouid=104294170867297406051&dls=true"
TOOL_LINK = "https://awwapp.com/#"
FOLDER_LINK = "https://drive.google.com/drive/u/1/folders/1tPd66fKZVvcHlzeR1yTJrLB12KFabVlW"

SCREENSHOT_PATH = os.path.join(
    os.getenv("HOME"), "Pictures", "U images", "SEA", "Evidencias 2020-2")
SESSION_DURATION_MIN = 120


def get_day_greeting():
    hour = datetime.datetime.now().hour
    if hour >= 15 and hour <= 19:
        return "Buenas tardes"
    elif hour > 19:
        return "Buenas noches"
    else:
        return "Buenos días"


class Tutorer(object):
    def __init__(self, *args):
        self.thread = threading.Event()
        self.time = datetime.datetime.now()
        self.ss_beep_file = os.path.join(
            os.getenv("HOME"), "Music", "alarm_beeps", "ss_beep.mp3")
        self.wakeup_beep_file = os.path.join(
            os.getenv("HOME"), "Music", "alarm_beeps", "beep_2.wav")
        self.dt = 0.75
        self.WhatsApp = WhatsApp()
        self.digest_args(*args)

    def __del__(self):
        self.thread.set()
        self.WhatsApp.__del__()

    def digest_args(self, *args):
        Screen("Tutorer", version="0.1.0").display()
        try:
            self.get_times()
            if any(map(lambda x: x.lower().startswith("en"), args)):
                self.suffix = "En"
                self.setup()
                self.wait_end_session()
            elif any(map(lambda x: x.lower().startswith("ex"), args)):
                self.suffix = "Ex"
                self.take_screenshot(
                    self.get_name(), TIME_DELAY - TIME_DELAY / 1.25)
                self.send_image(open_browser=True)

        except Exception as ex:
            print(f"[INFO] Something went wrong. {ex}")
            self.WhatsApp.__del__()
            return

    def wait_end_session(self):
        try:
            duration = input("Enter the session duration (in minutes): ")
            if duration == "":
                duration = SESSION_DURATION_MIN
            else:
                duration = int(duration)
            self.set_datetime(duration)
            print(
                f"[IN PROGRESS] Waiting {duration} minutes till the end of the session ...")
            while not self.thread.isSet():
                self.thread.wait(self.dt)
                if datetime.datetime.now() > self.time:
                    self.thread.set()
        except KeyboardInterrupt:
            print(f"[INFO] Keyboard Interruption detected.")
        except TypeError:
            print(f"[ERROR] Expected a number not {type(duration)}")
        try:
            threading.Thread(target=self.beep, args=(
                self.wakeup_beep_file, 5, 0.25)).start()
            input(f"[INFO] Press any key to take the screenshot ...")
            self.suffix = "Ex"
            self.take_screenshot(
                self.get_name(), TIME_DELAY - TIME_DELAY / 1.25)
            self.send_image(open_browser=True)

        except KeyboardInterrupt:
            print(f"[INFO] An interruption was detected, exiting ...")
            sys.exit()

    def get_name(self):
        self.name = f"{self.time.strftime(r'%Y-%m-%d')} {self.suffix}.jpg"
        return self.name

    def setup(self):
        Tutorer.open_pages()

        message = f"""{self.times["day greeting"]} muchachos, soy {TUTOR_NAME} y hoy {self.times["weekday"]} ({self.times["date"]}) estaré respondiendo a cualquier duda, pregunta e inquietud que tengan desde las {self.times["hour"][0]} {self.times["hour"][1]} hasta las {self.times["hour"][0] + SHIFT_TIME} {self.times["hour"][1]} 😀📚."""
        print("[IN PROGRESS] Copying greeting message to clipboard")
        pyperclip.copy(message)
        print("[INFO] Message ready to be posted")
        self.take_screenshot(self.get_name(), TIME_DELAY)
        self.send_image()

    def get_times(self):
        current_time = datetime.datetime.now()
        self.times = {}
        if current_time.hour > 12:
            self.times["hour"] = [current_time.hour - 12, "P.M."]
        else:
            self.times["hour"] = [current_time.hour, "A.M."]

        self.times["weekday"] = info.WEEKDAYS[current_time.weekday()]
        self.times["date"] = current_time.strftime(r"%d/%m/%Y")
        self.times["day greeting"] = get_day_greeting()

    def take_screenshot(self, ss_name, delay):
        print(f"[IN PROCESS] Waiting {delay}s to take the screenshot ...")
        time.sleep(delay)
        im = pyautogui.screenshot()
        Tutorer.beep(self.ss_beep_file, times=1)

        image = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        img_path = os.path.join(SCREENSHOT_PATH, ss_name)
        if not os.path.exists(img_path):
            cv2.imwrite(img_path, image)
        else:
            print(f"[INFO] {ss_name} already exists!")
            img_path = Tutorer.handle_repeat_file(img_path, suffix=self.suffix)
            cv2.imwrite(img_path, image)
        print(
            f"[INFO] Screenshot was taken successfully. Stored at {img_path}")
        time.sleep(1)
        self.ss_path = img_path

    def send_image(self, open_browser=False, delay=3):
        assert hasattr(self, "ss_path")
        if open_browser:
            self.WhatsApp.reopen()
        self.WhatsApp.send_messages({"Juliana": {"image": self.ss_path}})
        time.sleep(delay)
        self.WhatsApp.close()

    def set_datetime(self, interval_in_min):
        self.time = datetime.datetime.now() + datetime.timedelta(0, interval_in_min*60)
        return self.time

    @staticmethod
    def handle_repeat_file(path, suffix=""):
        ans = pyip.inputYesNo(
            prompt=f"Do you want to overwrite it? (y/n)\n", yesVal="y", noVal="n")
        if ans == "n":
            rename_suffix = 1
            while os.path.exists(path):
                path = path.replace(f"{suffix}.jpg", "") + \
                    f"{rename_suffix} {suffix}.jpg"
                suffix = f"{rename_suffix} {suffix}"
                rename_suffix += 1
        return path

    @staticmethod
    def copy_image_to_clipboard(im_path):
        im = Image.open(im_path)
        with BytesIO() as output:
            im.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
        print("[IN PROGRESS] Copying image to clipboard ...")
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        print("[INFO] Image ready to be sent")

    @staticmethod
    def open_pages():
        pages = ["Chrome", FOLDER_LINK, SPREADSHEET_LINK, TOOL_LINK, CHAT_LINK]
        print(f"[IN PROGRESS] Opening {len(pages)} pages ...")
        for page in pages:
            os.system(f"start /W /MAX {page}")

    @staticmethod
    def beep(sound_file, times=1, freq=0.1):
        try:
            it = 0
            while it < times:
                it += 1
                playsound.playsound(sound_file)
                time.sleep(freq)
        except playsound.PlaysoundException:
            print(f"{sound_file} is not a valid sound file.")
            return


if __name__ == "__main__":
    Tutorer(*sys.argv)
