import re, csv
from time import sleep, time
import random 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import winsound

class captcha():
    def __init__(self,driver):
        self.driver = driver
        self.main_page = driver.current_window_handle

    def solve_captcha(self):
        start = time()

        #get the first iframe
        self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[0])

        captcha_box = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID ,"recaptcha-anchor")))
        self.wait_response(0.5,0.7)
        #click on the box 
        captcha_box.click()
        #return to the main page
        self.driver.switch_to_window(self.main_page)
        self.wait_response(2,2.5)
        #next iframe
        self.driver.switch_to_frame(self.driver.find_elements_by_tag_name("iframe"[1]))

        #start the loop to solve the reCaptcha's picture puzzle

        i=1
        while i<130:
            print('\n\r{0}-th loop'.format(i))
            #move to the main page
            self.driver.switch_to_window(self.main_page)
            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME , 'iframe')))
            self.wait_response(1,2)
            if self.query_element_by_xpath('//span[@aria-checked="true"]'):
                winsound.Beep(400,1600)
                self.fill_csv(i, round(time() - start) - 1 )
                break
            
            self.wait_response(0.3, 1.5)
        
            #move to the next iframe to solve the puzzle
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[1])
            self.solve_puzzle()
            i += 1     

        
    def fill_csv(self,loops, time):
        with open('stat.csv', 'a', newline='') as statfile:
            writer = csv.writer(statfile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            writer.writerow([loops, time])

    def wait_response(self,start,end):
        rand = random.uniform(start, end)
        sleep(rand)

    def query_element_by_xpath(self,xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True
        #dimention of the picture
    def dimention(self):
        dim = int(self.driver.find_element_by_xpath('//div[@id="rc-imageselect-target"]/table').get_attribute("class")[-1])
        if dim:
            return dim
        else:
            return 3 #by default the dimention is 3

    #this method solve the reCaptcha's picture puzzle
    def solve_puzzle(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.ID, "rc-imageselect-target")))
        size = self.dimention()
        #check for previous clicked tiles
        if self.query_element_by_xpath('//div[@id="rc-imageselect-target"]/table/tbody/tr/td[@class="rc-imageselect-tileselected"]'):
            click = False
        else:
            click = True
        
        self.wait_response(0.5,1)

        img1 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(random.randint(1, size), random.randint(1, size)))))
        img1.click()
        if click:
            try:
                self.driver.find_element_by_xpath('//div[@id="rc-imagese;ect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(random.randint(1, size), random.randint(1, size))).click()
            except NoSuchElementException:
                print('\n\r No such Element Exception for finding 2nd image')

        #once completed the puzzle press the submit button
        self.driver.find_element_by_id("recaptcha-verify-button").click()

            