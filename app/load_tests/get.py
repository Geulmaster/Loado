from collections import UserString
import subprocess
from locust import HttpUser, task, between
from Loado.app import config_reader

configuration = config_reader()

class Config:

    def __init__(self, host = "localhost", port = "80",
     route = "/", users = str(5), spawn_rate = str(10),
      run_time = str(30)):
        if configuration:
            self.host = configuration["Load Testing"]["host"]
            self.port = configuration["Load Testing"]["port"]
            self.route = configuration["Load Testing"]["route"]
            self.users = configuration["Load Testing"]["users"]
            self.spawn_rate = configuration["Load Testing"]["spawn_rate"]
            self.run_time = configuration["Load Testing"]["run_time"]
        else:
            self.host = host
            self.port = port
            self.route = route
            self.users = users
            self.spawn_rate = spawn_rate
            self.run_time = run_time

conf_values = Config()

class GetLocust(HttpUser):

    wait_time = between(5, 15)

    @task
    def get(self):
        self.client.get(conf_values.route)