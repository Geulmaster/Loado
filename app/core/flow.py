import subprocess
from time import sleep
from selenium import webdriver
from Loado.app.load_tests.get import Config
from Loado.app.core.selectors import locust_selectors as sl
from Loado.app.load_tests import post
from Loado.app.load_tests import get

configuration = Config()

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

def general_flow(type):
    driver = webdriver.Chrome(options=options)
    subprocess.Popen(["locust", "-f", f"./load_tests/{type}.py", "--host", f"http://{configuration.host}:{configuration.port}"])
    driver.get("localhost:8089")
    driver.maximize_window()
    try:
        driver.find_element_by_id(sl.total_users_id).send_keys(configuration.users)
        driver.find_element_by_id(sl.spawn_rate_id).send_keys(configuration.spawn_rate)
        driver.find_element_by_xpath(sl.swarming_btn_xpath).click()
        sleep(configuration.run_time)
        driver.find_element_by_class_name(sl.stop_btn_class).click()
    except:
        print("One or more of the credentials is incorrect!")

def get():
    general_flow("get")

def post():
    general_flow("post")