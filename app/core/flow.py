import subprocess
from time import sleep
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Loado.app.load_tests.get import Config
from Loado.app.core.selectors import locust_selectors as sl

configuration = Config()
options = webdriver.ChromeOptions()

def general_flow(type):
    driver = webdriver.Chrome(options=options)
    run = subprocess.Popen(["locust", "-f", f"./load_tests/{type}.py", "--host", f"http://{configuration.host}:{configuration.port}"])
    driver.get("localhost:8089")
    driver.maximize_window()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, sl.total_users_id)))
    try:
        driver.find_element_by_id(sl.total_users_id).send_keys(configuration.users)
        driver.find_element_by_id(sl.spawn_rate_id).send_keys(configuration.spawn_rate)
        driver.find_element_by_xpath(sl.swarming_btn_xpath).click()
        sleep(int(configuration.time))
        driver.find_element_by_class_name(sl.stop_btn_class).click()
        print(driver.find_element_by_id("stats").text)
    except:
        print("One or more of the credentials is incorrect")
    run.kill()

def get():
    general_flow("get")

def post():
    general_flow("post")