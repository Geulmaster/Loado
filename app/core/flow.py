import subprocess
from pandas import DataFrame
from time import sleep
from json import loads
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Loado.app.load_tests.get import Config
from Loado.app.core.selectors import locust_selectors as sl

configuration = Config()
options = webdriver.ChromeOptions()

def export_results(result):
    """
    Empty results file and write new results to it
    """
    res_file = open("results.txt", "w")
    res_file.close()
    with open("results.txt", "w") as results_file:
        results_file.write(result)

def beautify_results():
    """
    Generates list of list for pandas.DataFrame
    """
    with open("results.txt", "r") as results_file:
        file_content = results_file.readlines()
    del file_content[0]
    values_list_of_list = []
    for line in file_content:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        values_list_of_list.append(line_list)
    return values_list_of_list

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
    print(new_results_dict)
    return new_results_dict
    
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
    driver.close()
    run.kill()

def get():
    general_flow("get")

def post():
    general_flow("post")