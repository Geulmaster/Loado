import subprocess
from pandas import DataFrame
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

def export_results(result):
    res_file = open("results.txt", "w")
    res_file.close()
    with open("results.txt", "w") as results_file:
        results_file.write(result)

def beautify_results():
    with open("results.txt", "r") as results_file:
        file_content = results_file.read()
    print(file_content.splitlines())

def general_flow(type):
    global driver
    driver = webdriver.Chrome(options=options)
    run = subprocess.Popen(["locust", "-f", f"./load_tests/{type}.py", "--host", f"http://{configuration.host}:{configuration.port}"])
    driver.get("localhost:8089")
    driver.maximize_window()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, sl.total_users_id)))
    #try:
    driver.find_element_by_id(sl.total_users_id).send_keys(configuration.users)
    driver.find_element_by_id(sl.spawn_rate_id).send_keys(configuration.spawn_rate)
    driver.find_element_by_xpath(sl.swarming_btn_xpath).click()
    sleep(int(configuration.time))
    driver.find_element_by_class_name(sl.stop_btn_class).click()
    results = driver.find_element_by_id("stats").text
    print(results)
    get_results()
    # except:
    #     print("One or more of the credentials is incorrect")
    driver.close()
    run.kill()

def get_results():
    columns_list = []
    columns = driver.find_elements_by_class_name("stats_label")
    for column in columns:
        columns_list.append(column.text)
    lines_list = []
    lines = driver.find_elements_by_xpath('//*[@id="stats"]/tbody/tr[1]')
    for line in lines:
        lines_list.append(line.text)
    for val in columns_list:
        if val == '':
            columns_list.remove(val)
    print(len(columns_list))
    print(len(lines_list))
    table = DataFrame(lines_list,columns=columns_list)
    print(table)
    
    

def get():
    general_flow("get")

def post():
    general_flow("post")