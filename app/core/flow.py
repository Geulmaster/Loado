import subprocess

subprocess.Popen(["locust", "-f", "../load_tests/get.py", "--host", "http://localhost:80"]).wait() 