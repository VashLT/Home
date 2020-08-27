from selenium.webdriver.common.keys import Keys
import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import reCaptcha_handler  

STUDENT_CODE = "2183075"

def main():
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://www.uis.edu.co/estudiantesWebJ8/autenticacion.jsf")

    # captcha = reCaptcha_handler.captcha(driver)
    time.sleep(2)
    student_code_box = driver.find_element_by_id("form:txtCodigoEstudiante")
    student_code_box.send_keys(STUDENT_CODE)
    time.sleep(2)
    system_box = driver.find_element_by_id("form:lstSistema")
    system_box.click()
    time.sleep(2)
    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "PREGRADO PRESENCIAL")))
    elem.click()
    time.sleep(3)

    # system_box = driver.find_element_by_id("form:lstSistema_input")
    
    # system_box.select_by_visible_text("PREGRADO PRESENCIAL")
  
    # program_box = Select(driver.find_element_by_id("form:lstPrograms_label"))
    # program_box.select_by_value("11")

    pass_box = driver.find_elements_by_id("form:txtContrasena")
    pass_box.send_keys("Chivasregal1")

    # submit = driver.find_elements_by_id("form:btnIngresar").click()
    
    
    time.sleep(3)

   
if __name__ == "__main__":
    main()