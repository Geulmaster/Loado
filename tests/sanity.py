import pytest
import subprocess
from time import sleep

def test_configurations_changes():
    run = subprocess.Popen(["python", "..\\app\\index.py", "-hn", "google.com"])
    sleep(1)
    run.kill()
