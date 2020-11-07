import subprocess
from Loado.app.load_tests.get import Config
from selenium import webdriver

configuration = Config()
driver = webdriver.Chrome()

def run_locust_page_get():
    subprocess.Popen(["locust", "-f", "./load_tests/get.py", "--host", f"http://{configuration.host}:{configuration.port}"])
    driver.get("localhost:8089")
