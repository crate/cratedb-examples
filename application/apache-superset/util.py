import requests

uri_login = "http://localhost:8088/api/v1/security/login"


def get_access_token():
    response = requests.post(uri_login, json={"username": "admin", "password": "admin", "provider": "db"})
    return response.json()["access_token"]


def get_auth_headers():
    access_token = get_access_token()
    return {"Authorization": f"Bearer {access_token}"}
