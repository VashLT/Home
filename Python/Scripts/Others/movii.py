from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



from time import sleep
import random
# see https://stackoverflow.com/questions/60296873/sessionnotcreatedexception-message-session-not-created-this-version-of-chrome
# from webdriver_manager.chrome import ChromeDriverManager

CREDENTIALS = {'celular': '3006557876', '':''}

class MOViiScrapper():
    def __init__(self, *args):
        self.url = "https://millondeusuarios.movii.com.co/#"
        self.digest_args(args)
    
    def digest_args(self, args):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument('--log-level=3')
        self.driver = webdriver.Chrome(chrome_options=options)

    def get_page(self):
        """Open a google chrome browser and log in"""
        self.driver.get(self.url)

        #click on buttons till get login credentials
        button_xpaths = ["//div//a[text()='LISTO']",
                         "//div//a[contains(@href,'#my')]",
                         "//div//a[text()='COMENZAR']"]
        for xpath in button_xpaths:
            elements = self.driver.find_elements_by_xpath(xpath)
            if len(elements) == 1:
                button = elements[0]
                sleep(1)
                button.click()
            else:
                for element in elements:
                    try:
                        sleep(1)
                        element.click()
                    except Exception as e:
                        print(f"[ERROR] : {e}")
        # self.input_credentials()
        self.testing()
        self.randomly_pick_a_galery()

    def input_credentials(self):
        """ enter data store in CREDENTIALS dict"""
        #phone
        input_phone_xpath = "//input[@name='phone']"
        button = self.driver.find_element_by_xpath(input_phone_xpath)
        submit_button = self.driver.find_element_by_xpath("//button[@type='submit']")
        sleep(1)
        button.send_keys(CREDENTIALS['celular'])
        submit_button.click()
    
    def testing(self):
        """Enter the galeries without participating"""
        button_xpath = "//a[contains(@class,'cont')]"
        self.driver.find_element_by_xpath(button_xpath).click()

        #pop up button
        page = EC.presence_of_element_located(
            (By.XPATH, "//div[@id='cboxOverlay']"))
        WebDriverWait(self.driver, 10).until(page)
        
        sleep(1)
        popup_xpath = "//a[contains(@class, 'realviewgal')]"
        popup = EC.presence_of_element_located((By.XPATH, popup_xpath))
        WebDriverWait(self.driver, 20).until(popup)
        self.driver.find_element_by_xpath(popup_xpath).click()


    def randomly_pick_a_galery(self):
        """ click on a galery and start selecting the iamges"""
        num_galeries = 10
        pages = 1000
        galerie = random.randint(1, 10)

        galerie_xpath = "//a[@href='%s']" % galerie
        self.driver.find_element_by_xpath(galerie_xpath).click()
        sleep(1)

        for page in range(1,pages + 1):
            sleep(2)
            container = self.driver.find_element_by_xpath("//div[@id='mygal']")
            self.process_html_source(container)
            #change page
            tip_xpath = "//i[contains(@class, 'right')]"
            self.driver.find_element_by_xpath(tip_xpath).click()

    
    def process_html_source(self, element):
        """ get html source code of a given element and search for
            win images """
        plain_html = element.get_attribute('innerHTML')
        with open("plain_html.txt", 'a') as sample:
            sample.write(plain_html)
        return plain_html


    def click_images(self, num_page):
        """click on every image in a given page, it assumes 
        number images per page is constant """
        cols = 4
        rows = 25
        for index in range(1, cols*rows + 1):
            img_common_xpath = "//img[@src='https://movii.isometri.co/c/500%s.jpg']" % index


        

if __name__ == "__main__":
    movii = MOViiScrapper()
    movii.get_page()
