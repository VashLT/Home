import threading
import datetime
import time
import inspect
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from utils import save_image_from_clipboard
# wait utils
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class WhatsAppUtils(object):
    @staticmethod
    def handle_exit(messages_func):
        def wrapper(self, messages):
            try:
                messages_func(self, messages)
            except Exception as ex:
                print(f"[ERROR] {ex}")
            finally:
                self.browser_thread.event.set()
        return wrapper

    @staticmethod
    def decorate_varnames(args_func):
        def wrapper(self, *args, **kwargs):
            """
                return args as a tuple and kwargs as a dict-like: {'varname': 'value'}
            """
            try:
                bound_args = inspect.signature(
                    args_func).bind(self, *args, **kwargs)
                bound_args.apply_defaults()
                parameters = dict(bound_args.arguments)
                return args_func(self, *parameters["args"], **parameters["kwargs"])
            except Exception as ex:
                self.browser_thread.event.set()

        return wrapper


class WhatsApp(webdriver.Chrome):
    def __init__(self, messages=None, opts=None, keep_open=True, session_path=None):
        """
            messages is a dict like:
                {'number/contact_name': {'message': '...', 'image': '...'}, ...}
        """
        # attrs
        self.options = webdriver.ChromeOptions()
        self.browser_thread = threading.Thread(
            target=self.keep_browser, args=(100,))
        self.browser_thread.event = threading.Event()

        self.digest_args(chrome_options=[
                         "start-maximized", "disable-infobars", "--headless"], session_path=session_path, keep_open=keep_open)
        self.url = "https://web.whatsapp.com/"
        super().__init__(options=self.options)
        self.get(self.url)
        if messages:
            self.send_messages(messages)

    def __del__(self):
        self.quit()
        self.browser_thread.event.set()

    def reopen(self):
        super().__init__(options=self.options)
        self.get(self.url)
        return self

    @WhatsAppUtils.decorate_varnames
    def digest_args(self, *args, **kwargs):
        chrome_profile = os.path.join(os.getenv(
            "HOME"), "AppData", "Local", "Google", "Chrome", "User Data", "Profile 1")
        session_path = os.path.join(
            os.getenv("HOME"), "Home", "Python", "Scripts", "Tutorer")

        for varname, value in kwargs.items():
            if varname is "opts":
                # "--headless"]
                [self.options.add_argument(arg) for arg in value]
            elif varname is "session_path":
                session_path = value
            elif varname is "keep_open" and not value:
                self.browser_thread.start()
        self.options.add_argument(f"user-data-dir={session_path}")

    @WhatsAppUtils.handle_exit
    def send_messages(self, messages):
        """
            Ways to specify an image to send:
                Image path, then in messages-dict must be specified as 'image': 'path/to/image'
                Image lies on clipboard, then in messages-dict must be specified as 'image': True
        """
        try:
            self.init_use_elements()
            if not isinstance(messages, dict):
                raise Exception("messages must be a dictionary")
            for identifier, data in messages.items():
                # TODO: add functions to handle slow response of the page
                identifier = identifier.replace("�", '')
                if not isinstance(data, dict):
                    self.send_message(identifier, data)
                else:
                    for mssg_type, content in data.items():
                        if mssg_type.lower() == "message":
                            self.send_message(identifier, content)
                        elif mssg_type.lower() == "image":
                            self.send_image(identifier, content)
        except Exception as ex:
            print(f"[ALERT] {ex}")

    def init_use_elements(self):
        self.search_box = self.wait_for_element_by_xpath(
            "//div[starts-with(@class, '_2_1')]")

    def wait_for_element_by_xpath(self, xpath, max_time=60, delay=1):
        try:
            max_time = datetime.datetime.now() + datetime.timedelta(0, max_time)
            while datetime.datetime.now() < max_time:
                try:
                    element = self.find_element_by_xpath(xpath)
                    time.sleep(delay)
                    return element
                except NoSuchElementException:
                    continue
            raise Exception(f"Exceeded expected wait time.")
        except Exception as ex:
            print(f"[ERROR] Something went wrong. {ex}")

    def get_contact_element(self, name_or_number, max_time=20):
        try:
            contact_xpath = "//span[contains(@title,'%s')]/ancestor::div[starts-with(@class, '_2Z' )]" % (
                name_or_number,)
            contact = self.wait_for_element_by_xpath(
                contact_xpath, max_time=max_time)
            return contact

        except NoSuchElementException:
            # TODO: implement another try by searching the contact in the WhatsApp contact's searcher
            print(
                f"[INFO] No contact/group named {name_or_number} was found. ")
            return

    def send_message(self, identifier, msg):
        contact = self.get_contact_element(identifier)
        if not contact:
            print(f"[INFO] Message to {identifier} couldn't be sent.")
            return
        contact.click()
        self.mssg_box = self.find_element_by_xpath(
            "//div[contains(text(), 'Escribe')]//following-sibling::div")
        self.mssg_box.send_keys(msg, Keys.ENTER)

    def send_image(self, identifier, data, delay=2):
        try:
            path = data
            if isinstance(data, bool) and data:
                path = self.create_temp_path()
                del_at_end = True
            if not os.path.exists(path):
                raise Exception("Image path doesn't exist.")
            contact = self.get_contact_element(identifier)
            contact.click()
            time.sleep(delay)
            print(f"[IN PROGRESS] Sending image ...")

            self.wait_for_element_by_xpath(
                "//div[@title='Adjuntar']", max_time=10).click()
            self.find_element_by_css_selector(
                "input[type='file']").send_keys(path)

            time.sleep(delay)
            self.find_element_by_xpath(
                "//span[@data-testid = 'send']/ancestor::div[@role = 'button']").click()
            time.sleep(delay * 3)
            print(f"[INFO] The image was sent to {identifier} successfully.")
            if 'del_at_end' in locals():
                os.remove(path)

        except InvalidArgumentException as ex:
            print(f"[ALERT] The image path: {data} is not valid. {ex}")
            return
        except Exception as ex:
            print(f"[ALERT] {ex}")

    def create_temp_path(self, temp_name="Hzksiqk_2=09"):
        """
            save image that is stored in clipboard and later on it deletes it.
        """
        path = save_image_from_clipboard(os.path.join(
            os.getenv("HOME"), "Documents"), temp_name)
        return path

    def keep_browser(self, timeout=20, delta_t=0.75):
        timeout = datetime.datetime.now() + datetime.timedelta(0, timeout*60)
        while not self.browser_thread.event.isSet():
            if datetime.datetime.now() > timeout:
                self.browser_thread.event.set()
            else:
                self.browser_thread.event.wait(delta_t)


if __name__ == "__main__":
    # example use
    data = {"Agenda 💪": {"message": "Example Message",
                         "image": "C:/Users/jose2/Pictures/Jose.jpg"}}
    WhatsApp(data)
