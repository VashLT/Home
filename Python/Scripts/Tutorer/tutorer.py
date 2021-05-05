#!python3
from imports import *

# libraries and modules
__all__ = [
    "datetime",
    "pyperclip",
    "cv2",
    "sys",
    "pyautogui",
    "os",
    "info",
    "configparser",
    "time",
    "WhatsApp",
    "playsound",
    "threading",
    "traceback",
    "pause",
    "BytesIO",
    "win32clipboard",
    "numpy as np",
    "pyinputplus as pyip",
    "Modules.Screen.Screen",
]


def path_it(folders):
    return os.path.join(os.getenv('HOME'), *folders)


CONFIG = path_it(["Home", "Python", "Scripts", "Tutorer", "config.ini"])

# pylint:disable=undefined-variable


class Tutorer(object):
    def __init__(self, *args):
        self.arg_parser = configparser.ConfigParser()
        with open(CONFIG, encoding="utf-8") as config_file:
            self.arg_parser.read_file(config_file)
        self.thread = threading.Event()
        self.time = datetime.datetime.now()
        self.WhatsApp = WhatsApp()
        self.settings()
        self.parse_args(*args)

    def __del__(self):
        self.thread.set()
        self.WhatsApp.__del__()

    def settings(self):
        # from .ini file

        self.TUTOR = self.arg_parser['TUTOR']
        self.META = self.arg_parser['META']
        self.EXTRA = self.arg_parser['EXTRA']
        self.STORAGE = self.arg_parser['STORAGE']
        self.LINKS = self.arg_parser['LINKS']

        self.log_path = path_it(eval(self.STORAGE['log file']))
        self.log = Logger(
            path_log_file=self.log_path)

        self.ss_path = path_it(eval(self.STORAGE['screenshot']))

        self.ss_beep_file = path_it(eval(self.EXTRA['beep start file']))

        self.wakeup_beep_file = path_it(
            eval(self.EXTRA['beep end file'])
        )
        self.pages = [link for link in self.LINKS.values()]

    def parse_args(self, *args):
        self.test_mode = False
        if any([arg in args for arg in ["-t", "--test"]]):
            self.test_mode = True
        try:
            Screen("Tutorer", version="0.1.0").display()
            self.get_times()
            if any([arg in args for arg in ["-o", "--out", "-e", "--exit"]]):
                self.suffix = "Ex"
                self.msg = "Adjunto el pantallazo de salida: "
                time_delay = float(self.META['screenshot delay'])
                img_path = self.get_ss_path()
                self.take_screenshot(img_path, time_delay - time_delay / 1.25)
                self.send_image(img_path, entry=True)

            elif self.test_mode and any([arg in args for arg in ["-i", "--image"]]):
                self.suffix = "Test"
                self.msg = "Testing ..."
                img_path = self.get_ss_path()
                self.take_screenshot(img_path, 1)
                self.send_image(img_path)
            else:
                self.suffix = "En"
                self.msg = "Adjunto el pantallazo de entrada: "
                self.setup()
                self.wait_end_session()

        except Exception as ex:
            self.log.exception(
                f"TYPE: <{type(ex)}> - {ex}\n", traceback.format_exc())
            print(
                f"Something went wrong. Check {self.log_path} for more info.")
        finally:
            self.thread.set()

    def wait_end_session(self, dt=0.75):
        try:
            duration = pyip.inputNum(
                "Enter the session duration (in minutes): ", min=0)
            if duration == "":
                duration = self.META['session duration']
            else:
                duration = int(duration)
            self.set_time_interval(duration)
            print(
                f"[IN PROGRESS] Waiting {duration} minutes till the end of the session ...")
            while not self.thread.isSet():
                self.thread.wait(dt)
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
            time_delay = float(self.META['screenshot delay'])
            img_path = self.get_ss_path()
            self.take_screenshot(img_path, time_delay - time_delay / 1.25)
            self.send_image(img_path, open_browser=True, entry=False)

        except KeyboardInterrupt:
            print(f"[INFO] An interruption was detected, exiting ...")
            sys.exit()

    def get_ss_path(self):
        name = f"{self.time.strftime(r'%Y-%m-%d')} {self.suffix}.jpg"
        path = os.path.join(self.ss_path, name)
        if os.path.exists(path):
            print(f"[INFO] {name} already exists!")
            return Tutorer.handle_repeat_file(path, suffix=self.suffix)
        return path

    def setup(self):
        Tutorer.open_pages(self.pages)

        name = self.TUTOR['name']
        shift_time = int(self.META['strip duration'])

        message = f"""{self.times["day greeting"]} muchachos, soy {name} y hoy {self.times["weekday"]} ({self.times["date"]}) estaré respondiendo a cualquier duda, pregunta e inquietud que tengan desde las {self.times["hour"][0]} {self.times["hour"][1]} hasta las {self.times["hour"][0] + shift_time} {self.times["hour"][1]} 😀📚."""
        print("[IN PROGRESS] Copying greeting message to clipboard")
        pyperclip.copy(message)
        print("[INFO] Message ready to be posted")
        img_path = self.get_ss_path()
        self.take_screenshot(img_path, float(self.META['screenshot delay']))
        try:
            self.send_image(img_path)
        except Exception as ex:
            self.log.exception(
                f"TYPE: <{type(ex)}> - {ex}\n", traceback.format_exc())
            print(
                f"Couldn't send image. Check {self.log_path} for more info.")
            return

    def get_times(self):
        current_time = datetime.datetime.now()
        self.times = {}
        if current_time.hour > 12:
            self.times["hour"] = [current_time.hour - 12, "P.M."]
        else:
            self.times["hour"] = [current_time.hour, "A.M."]

        if 60 - current_time.minute <= float(self.META["round time"]):
            self.times["hour"][0] += 1

        self.times["weekday"] = info.WEEKDAYS[current_time.weekday()]
        self.times["date"] = current_time.strftime(r"%d/%m/%Y")
        self.times["day greeting"] = Tutorer.greeting_time()

    def take_screenshot(self, store_path, wait_time=None):
        delay = wait_time or float(self.META['screenshot'])
        print(f"[IN PROCESS] Waiting {delay}s to take the screenshot ...")
        time.sleep(delay)
        im = pyautogui.screenshot()
        Tutorer.beep(self.ss_beep_file, times=1)

        image = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        cv2.imwrite(store_path, image)
        print(
            f"[INFO] Screenshot was taken successfully. Stored at {store_path}")
        time.sleep(1)

    def send_image(self, path, open_browser=False, delay=3, entry=True):
        assert hasattr(self, "ss_path")
        if open_browser:
            self.WhatsApp = self.WhatsApp.reopen()
        to = self.TUTOR['juliana whatsapp']
        if self.test_mode:
            to = self.META['test whatsapp']

        self.WhatsApp.send_messages(
            {to: {"message": self.msg, "image": path}})
        time.sleep(delay * 2)
        self.WhatsApp.close()

    def set_time_interval(self, interval):
        """ Interval of time in minutes """
        self.time = datetime.datetime.now() + datetime.timedelta(0, interval*60)
        return self.time

    @ staticmethod
    def handle_repeat_file(path, suffix=""):
        ans = pyip.inputYesNo(
            prompt=f"Do you want to overwrite it? (y/n)\n", yesVal="y", noVal="n")
        if ans == "n":
            rename_suffix = 1
            old_suffix = suffix
            while os.path.exists(path):
                new_suffix = " ".join([str(rename_suffix), suffix])
                path = path.replace(old_suffix, new_suffix)
                old_suffix = new_suffix
                rename_suffix += 1
        return path

    @ staticmethod
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

    @ staticmethod
    def open_pages(pages):
        pages.insert(0, "Chrome")
        print(f"[IN PROGRESS] Opening {len(pages)} pages ...")
        for page in pages:
            os.system(f"start /W /MAX {page}")

    @ staticmethod
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

    @ staticmethod
    def greeting_time():
        hour = datetime.datetime.now().hour
        if hour >= 12 and hour <= 19:
            return "Buenas tardes"
        elif hour >= 19:
            return "Buenas noches"
        else:
            return "Buenos días"


if __name__ == "__main__":
    Tutorer(*sys.argv)
    # Debug
    # Tutorer("", "-t")
    # path = os.path.join(os.getenv("HOME"), "Pictures", "U images",
    #                     "SEA", "Evidencias 2020-2", "2021-03-12 Test.jpg")
    # Tutorer.handle_repeat_file(path, suffix="Test")
