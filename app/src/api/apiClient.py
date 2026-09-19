import requests

class ApiClient:

    def __init__(self, baseUrl="http://127.0.0.1:8000"):
        self.baseUrl = baseUrl

    def createUser(self, userName, psw):

        response = requests.post(
            f"{self.baseUrl}/users",
            json={
                "userName": userName,
                "psw": psw
            },
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    def getMeals(self, plannerId):

        response = requests.get(
            f"{self.baseUrl}/meals",
            params={
                "plannerId": plannerId
            },
            timeout=5
        )

        response.raise_for_status()

        return response.json()