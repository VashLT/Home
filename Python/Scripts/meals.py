from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

from pathlib import Path
from Modules.Screen.Screen import Screen
import logging
import time
import os
import requests
import sys
import configparser

#! Python3

# Meal register, version: 0.1
"""
    This script register my regular meals on the myfitnesspal web
"""

# INPUT None
# OUTPUT None
PATH = Path(Path.home() / "Documents" /
            "Home" / "Python" / "Scripts" / "meal_debug")
DEFAULT_DEBUG_PATH = PATH / "debug.txt"
# clean debug file
os.remove(DEFAULT_DEBUG_PATH)
logging.basicConfig(filename=DEFAULT_DEBUG_PATH,
                    level=logging.DEBUG, format="%(asctime)s - %(message)s")
# logging.disable(logging.CRITICAL)

# this is intended to be a quickly way to add funcionalities to myfitnesspal class
FEATURES = ["add", "delete"]


class myfitnesspal():
    def __init__(self, args):
        """ args are parse as add, or delete"""
        self.url = "https://www.myfitnesspal.com/"
        self.screen = Screen("Meal manager", version='0.1')
        # order matters
        self.meals = {"Desayuno": 0, "Media Mañana": 1,
                      "Almuerzo": 2, "Media tarde": 3, "Cena": 4}
        self.translate(language="spanish")
        self.digest_args(args)

    def usage(self):
        usage = """
        Usage: $meals add   *meal-name *meal-name ...:   (add the regular ingredients for each given meal)
                      delete meal-name:                  (delete an existing meal ingredients)
        """
        print(usage)

    def translate(self, language="spanish"):
        """ Handle the random modification of languages in myfitnesspal website """
        config_path = PATH / "config.ini"
        assert os.path.exists(config_path)
        parser = configparser.ConfigParser()
        parser.read(config_path, encoding="utf-8")
        self.parser = parser[language]

    def digest_args(self, args):
        self.screen.display()
        if len(args) < 2:
            self.usage()

        task = args[1]
        if task in FEATURES:

            print("[IN PROGRESS] Loading page...")
            self.get_page()
            print("[INFO] Web page loaded succesfully.")
            time.sleep(1)
            self.LogIn()
            time.sleep(3)

            self.get_foods_page()
            time.sleep(3)

            args = [arg.lower().capitalize() for arg in args]
            if task == "add":
                meals = args[2:]
                self.add_meal(meals)
            elif task == "delete":
                # parse meals like 'media tarde' or 'media mañana'
                if args[2] == "Media":
                    meal = " ".join([args[2], args[3].lower()])
                else:
                    meal = args[2]
                self.delete_meal(meal)
        else:
            self.usage()

        print(f"Thanks for using the script!")
        sys.exit()

    def add_meal(self, meals, regular=True):
        """ Handle the register of meals  """
        # parse each element in meals list
        temp_meals = []
        for index, meal in enumerate(meals):
            if meal == "Media":
                meal += " " + meals[index + 1].lower()
            elif meal == "Tarde" or meal == "Mañana":
                continue
            temp_meals.append(meal)

        meals = temp_meals
        logging.debug(f"Meals {meals}")
        for meal in meals:
            if meal in self.meals.keys():
                #new or regular
                if regular:
                    regular_meal = self.get_regulars(meal)
                    self.add_ingredients(meal, regular_meal)
            else:
                print(f"[INFO] {meal} is not a correct meal.")

    def delete_meal(self, meal):
        try:
            if not meal in self.meals.keys():
                raise Exception("Meal not available.")

            amount_elements = len(self.get_regulars(meal))

            meal_header = self.get_header(meal)
            # delete button
            button, name = self.get_ingredient_to_delete(meal_header)
            if not button:
                print(f"[INFO] No entries were found for {meal}.")
                return

            print("[IN PROGRESS] Removing ingredients ...")
            while button:
                button.click()
                print(f"     [INFO] {name} Succesfully removed.")
                meal_header = self.get_header(meal)
                button, name = self.get_ingredient_to_delete(meal_header)
            print(f"[INFO] {meal} Ingredients removed succesfully.")

        except Exception as ex:
            print(f"[ERROR] {ex}")

    def get_header(self, meal):
        try:
            # wait for page to be scrapped
            food_page = EC.presence_of_element_located(
                (By.XPATH, "//tr[contains(@class,'meal_header')]"))
            WebDriverWait(self.driver, 10).until(food_page)
        except TimeoutException:
            print(
                f"[ERROR] {self.driver.current_url} took too much time to load")

        # TODO: Solve wrong parent element, two options: *Figure out how to access to the container element, *Split the header matching to divide access to external headers and matched header.
        headers = self.driver.find_elements_by_xpath(
            "//tr[@class = 'meal_header']")
        assert len(headers) == 6
        for header in headers:
            try:
                if header.find_element_by_xpath(".//td[text() = '%s']" % meal):
                    return header
            except NoSuchElementException:
                continue

    def get_ingredient_to_delete(self, node):
        """ Find nodes at the same level according to a certain conditions"""
        sibling = node.find_elements_by_xpath(".//following-sibling::tr")
        if not sibling:
            return [None, None]  # avoid to unpack a unique None value

        element = sibling[0]  # always select the top element
        try:
            delete_button = element.find_element_by_xpath(
                ".//td[@class = 'delete']")
            name = element.find_element_by_xpath(
                ".//td[@class = 'first alt']").text
            return [delete_button, name]
        except NoSuchElementException:
            return [None, None]  # avoid to unpack a unique None value
        except Exception as ex:
            print(f"[ERROR] {ex}")

    def get_regulars(self, meal):
        # default meals for a breakfast
        BREAKFAST_REGULAR = [
            "Latti - Leche Descremada-deslactosada",
            "Facundo - Champiñones Tajados",
            "Natri - Galletas Multicereal Tostadas",
            "Genereico - Pechuga De Pollo (Sin Piel Ni Hueso)",
            "Justo Y Bueno - Jamón Sanduche Ahumado",
            "mas por menos - queso bajo en grasa",
            "SUSANITA - Tostadas de Arroz Con Sal Marina",
            "Homemade - Huevo Frito",
        ]
        MIDDLE_MORNING_REGULAR = []
        LUNCH_REGULAR = [
            "Lentejas Schettino - Lentejas Cocidas",
            "Verdura - Papa Cocida",
            "mercaderia - Mostaza",
            "Arju - Ensalada Tomate-cebolla-lechuga-pepinos",
            "Fruco - Salsa De Tomate",
            "Mercadería - Mayonesa Baja en grasa",
            "Pechuga de pollo (sin hueso, sin piel)",
            "Arroz Blanco Daniba - Arroz Blanco Cocido",

        ]
        MIDDLE_AFTERNOON_REGULAR = [
            "Nuthos - Mezcla Crunchy",
            "Mash - Creamy Peanut Buttet",
        ]
        DINNER_REGULAR = [
            "Latti - Leche Entera",
            "Latti - Leche Descremada-deslactosada",
            "Servipan - Pan De Queso",
            "Coolechera - Queso Costeño",
            "mercaderia - Mostaza",
            "Fruco - Salsa De Tomate",
            "Arju - Ensalada Tomate-cebolla-lechuga-pepinos",
            "Genereico - Pechuga De Pollo (Sin Piel Ni Hueso)",
        ]

        index = self.meals[meal]
        if index == 0:
            return BREAKFAST_REGULAR
        elif index == 1:
            return MIDDLE_MORNING_REGULAR
        elif index == 2:
            return LUNCH_REGULAR
        elif index == 3:
            return MIDDLE_AFTERNOON_REGULAR
        elif index == 4:
            return DINNER_REGULAR

    def get_page(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        # options.add_argument('--headless')
        options.add_argument('--log-level=3')
        # options.add_argument("--disable-logging")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(self.url + "account/login")

    def LogIn(self):
        print("[IN PROGRESS] Log In account...")

        try:
            # let the page load
            time.sleep(3)

            # save the main window
            src_window = self.driver.window_handles[0]

            # wait the fb login button to load
            log_in_frame_xpath = "//div[contains(@class,'fb-login-button')]"
            log_in_iframe = EC.element_to_be_clickable(
                (By.XPATH, log_in_frame_xpath))
            WebDriverWait(self.driver, 20).until(log_in_iframe).click()

            # pop-up page
            pop_up_fb_page = self.driver.window_handles[1]
            self.driver.switch_to_window(pop_up_fb_page)

            user_box = self.driver.find_element_by_id("email")
            user_box.send_keys("jj_silvaa@hotmail.com")

            pw_box = self.driver.find_element_by_id("pass")
            pw_box.send_keys("Chivasregal123")

            time.sleep(3)
            self.driver.find_element_by_name("login").click()
            time.sleep(2)
            self.driver.switch_to_window(src_window)
            print("[INFO] Log In complete.")

        except Exception as ex:
            print(f"[ERROR] Log In proccess has failed. {ex}")

    def get_foods_page(self):

        # wait until iframe be clickeable
        logging.debug(f"Number of windows {len(self.driver.window_handles)}")
        while True:
            try:
                close_button = EC.visibility_of_element_located(
                    (By.XPATH, "//a[@class = 'close-btn' and text() = '✕']"))
                popup_box = WebDriverWait(self.driver, 20).until(close_button)
                popup_box.click()
                break

            except ElementNotInteractableException:
                continue
            except TimeoutException:
                print(
                    f"[ERROR] {self.driver.current_url} took too much time to load")
                continue
            except Exception as ex:
                print(f"[ERROR] Can't close the pop-up box. {ex}")
                break
        time.sleep(1)
        # get meals page
        FOOD_button = self.driver.find_element_by_xpath(
            "//a[text() = 'Alimento']")
        FOOD_button.click()

    def add_ingredients(self, meal, ingredients):
        try:
            # wait for page to be scrapped
            food_page = EC.presence_of_element_located(
                (By.XPATH, "//tr[contains(@class,'meal_header')]"))
            WebDriverWait(self.driver, 10).until(food_page)
        except TimeoutException:
            print(
                f"[ERROR] {self.driver.current_url} took too much time to load")

        buttons = self.driver.find_elements_by_xpath(
            "//a[contains(@href,'/food/add to diary?meal=') or text() = '%s']" % self.parser.get("FOOD_BUTTON"))
        # TODO: find all All Food buttons.
        assert len(buttons) == 6

        buttons[self.meals[meal]].click()

        time.sleep(3)
        print(f"[IN PROGRESS] Adding ingredients for {meal}...")
        # get all the regular foods
        regular_ingredients_xpath = "//tr[@class = 'favorite']"
        regular_ingredients = self.driver.find_elements_by_xpath(
            regular_ingredients_xpath)
        for ingredient in ingredients:
            self.add_ingredient(ingredient, regular_ingredients)

        time.sleep(2)
        submit_button = self.driver.find_element_by_xpath(
            "//input[@id = '%s']" % self.parser.get("SUBMIT_BUTTON"))
        submit_button.click()

        print("[INFO] Added ingredients succesfully.")

    def add_ingredient(self, ingredient, iterator):

        target_xpath = ".//td[text() = '%s']" % ingredient

        for regular_ingredient in iterator:
            logging.debug(f"xpath = {target_xpath}")
            try:
                target_ingredient = regular_ingredient.find_element_by_xpath(
                    target_xpath)
                if target_ingredient:
                    # add it
                    regular_ingredient.find_element_by_xpath(
                        ".//input[@class = 'checkbox']").click()
                    print(
                        f"     [INFO] Added {target_ingredient.text} succesfully.",)
                    break
            except NoSuchElementException:
                continue
            except ElementNotInteractableException:
                continue
            except Exception as ex:
                logging.debug(f"[ERROR] in {regular_ingredient} CAUSE: {ex}")
                print(f"[ERROR] Something was wrong - {type(ex)} {ex}")
                break
        logging.debug(f"target ingredient {target_ingredient.text}")


if __name__ == "__main__":
    myfitnesspal(sys.argv)
