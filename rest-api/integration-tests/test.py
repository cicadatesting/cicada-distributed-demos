import os

import requests
import uuid

from cicadad.core.decorators import dependency, scenario
from cicadad.core.engine import Engine

# NOTE: uncomment for testing docker vs local executors
# DEMO_API_ENDPOINT = "http://172.17.0.1:8080"
# DEMO_API_ENDPOINT = "http://demo-api:8080"
DEMO_API_ENDPOINT = "http://localhost:8080"

engine = Engine()


@scenario(engine)
def post_user(context):
    print("os.env", os.environ)
    email = f"{str(uuid.uuid4())[:8]}@gmail.com"

    response = requests.post(
        url=f"{DEMO_API_ENDPOINT}/users",
        json={
            "name": "jeremy",
            "age": 23,
            "email": email,
        },
    )

    assert response.status_code == 200
    body = response.json()

    return {"email": email, "id": body["id"]}


@scenario(engine)
@dependency(post_user)
def post_user_duplicate_email(context):
    response = requests.post(
        url=f"{DEMO_API_ENDPOINT}/users",
        json={
            "name": "jeremy",
            "age": 23,
            "email": context["post_user"]["output"]["email"],
        },
    )

    assert response.status_code == 400, f"Status code is {response.status_code}"


@scenario(engine)
@dependency(post_user)
def get_user(context):
    response = requests.get(
        url=f"{DEMO_API_ENDPOINT}/users/{context['post_user']['output']['id']}",
    )

    assert response.status_code == 200


@scenario(engine)
def get_user_not_found(context):
    response = requests.get(
        url=f"{DEMO_API_ENDPOINT}/users/0",
    )

    assert response.status_code == 404


if __name__ == "__main__":
    engine.start()
