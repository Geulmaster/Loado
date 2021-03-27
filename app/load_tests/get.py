from collections import UserString
from locust import HttpUser, task, between
from Loado.app.load_tests import Config

conf_values = Config()

class GetLocust(HttpUser):

    wait_time = between(5, 15)

    @task
    def get(self):
        self.client.get(conf_values.route)
        