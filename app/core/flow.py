import subprocess
from Loado.app.load_tests.get import Config
from selenium import webdriver

configuration = Config()

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

def get():
    driver = webdriver.Chrome(options=options)
    subprocess.Popen(["locust", "-f", "./load_tests/get.py", "--host", f"http://{configuration.host}:{configuration.port}"])
    driver.get("localhost:8089")
