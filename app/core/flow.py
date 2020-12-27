import subprocess
from pandas import DataFrame
from time import sleep
from json import loads
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Loado.app.load_tests.get import Config
from Loado.app.core.selectors import locust_selectors as sl
from Loado.app.core import export_results, beautify_results
from Loado.app.core.data_wizard import Mongo

configuration = Config()
options = webdriver.ChromeOptions()

results = beautify_results()

def get_results():
    """
    Return results table from locust's UI
    """
    columns_list = []
    columns = driver.find_elements_by_class_name(sl.stats_label_class)
    for column in columns:
        columns_list.append(column.text)
    formatted_columns = [x for x in columns_list if x]
    table = DataFrame([results[0]],columns=formatted_columns)
    print(table)
    return table

def convert_results_to_json():
    """
    Gets an unformatted dict and formats it in order to push to DB
    """
    global new_results_dict
    result = get_results().to_json(orient="split")
    parsed_result = loads(result)
    columns = parsed_result["columns"]
    data = parsed_result["data"]
    formatted_data = []
    for sublist in data:
        for item in sublist:
            formatted_data.append(item)
    new_results_dict = {}
    for i, val in enumerate(columns):
        new_results_dict[val] = formatted_data[i]
    new_results_dict["_id"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print(new_results_dict)
    return new_results_dict

def insert_results_to_db():
    """
    Inserts results to DB - uses user's input for permission
    """
    db = Mongo()
    push = input("Would you like to save results in DB? ")
    if push.lower() == "y":
        db.insert_to_mongodb(doc=new_results_dict)
    else:
        print("OK!")
    
def general_flow(type):
    """
    Runs load tests accordint to type
    """
    global driver
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
        results = driver.find_element_by_id(sl.results_id).text
        export_results(results)
        convert_results_to_json()
    except:
        print("One or more of the credentials is incorrect")
    finally:
        driver.close()
        insert_results_to_db()
        run.kill()

def get():
    general_flow("get")

def post():
    general_flow("post")