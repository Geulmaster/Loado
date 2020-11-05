import subprocess
from locust import HttpUser, task, between
from Loado.app import config_reader

configuration = config_reader()

class GetLocust(HttpUser):

    def __init__(self, host = "localhost", port = "80", route = "/"):
        if configuration:
            self.host = configuration["Load Testing"]["host"]
            self.port = configuration["Load Testing"]["port"]
            self.route = configuration["Load Testing"]["route"]
        else:
            self.host = host
            self.port = port
            self.route = route

    @task
    def get(self):
        self.client.get(self.route)