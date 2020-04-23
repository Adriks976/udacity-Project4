from locust import HttpLocust, TaskSet, task, between
import json


class UserBehavior(TaskSet):
    

    @task
    def put_tests(self):
        payload = {
            "CHAS": {
                "0": 0
            },
            "RM": {
                "0": 6.575
            },
            "TAX": {
                "0": 296.0
            },
            "PTRATIO": {
                "0": 15.3
            },
            "B": {
                "0": 396.9
            },
            "LSTAT": {
                "0": 4.98
            }
        }
        self.client.post("/predict", json=payload)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5.0, 9.0)