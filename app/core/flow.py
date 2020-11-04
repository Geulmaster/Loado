import subprocess
import webbrowser as web
import pyautogui as pg
from Loado.app.load_tests.get import GetLocust

get_test = GetLocust()

def run_locust_page_get():
    subprocess.Popen(["locust", "-f", "../load_tests/get.py", "--host", f"http://{get_test.host}:{get_test.port}"]).wait()
    web.open('localhost:8089')
    pg.press('enter')