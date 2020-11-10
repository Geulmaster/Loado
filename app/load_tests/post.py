import json
from locust import HttpUser, task, between
from Loado.app.load_tests import Config

conf_values = Config()

def load_json():
    with open("./core/post_body.json") as json_file:
        json_dict = json.load(json_file)
    return json_dict

conf_dict = load_json()

class PostLocust(HttpUser):

    wait_time = between(5, 15)

    @task
    def post(self):
        self.client.post(conf_values.route, json=conf_dict)