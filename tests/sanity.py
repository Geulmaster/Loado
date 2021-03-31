import pytest
import subprocess
from time import sleep

class TestSanity:

    @pytest.mark.order1
    def test_args(self, name, arg):
        assert name is not None
        assert arg is not None
        print(f"Name is {name}")
        print(f"Argument is {arg}")


    @pytest.mark.order2   
    def test_configurations_changes(self, name="https://google.com", arg="hn"):
        run = subprocess.Popen(["python", "..\\app\\index.py", f"-{arg}", name])
        sleep(1)
        run.kill()

"""
Run example:
pytest -q sanity.py --arg hn --name https://google.com
"""