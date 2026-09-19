import requests

from PySide6 import QtCore, QtWidgets
from login.loginPage import LoginPage
from login.accountCreationPage import AccountCreationPage
from gui.smartphone import SmartphoneApi
from plannerList.plannerListPage import PlannerListPage


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.apiUrl = "mealplanner-production-e25d.up.railway.app"

        self.userId = None
        self.currentPlannerId = None
        self.token = None

        self.settings = QtCore.QSettings(
            "MealPlanner",
            "MealPlanner"
        )

        self.createWidgets()
        self.createConnections()
        self.restoreSession()

    # =====================================================
    # WIDGETS
    # =====================================================

    def createWidgets(self):

        self.pages = QtWidgets.QStackedWidget()

        self.loginPage = LoginPage()

        self.accountCreationPage = AccountCreationPage()

        self.plannerListPage = PlannerListPage()

        self.calendarPage = SmartphoneApi()

        self.pages.addWidget(
            self.loginPage
        )

        self.pages.addWidget(
            self.accountCreationPage
        )

        self.pages.addWidget(
            self.plannerListPage
        )

        self.pages.addWidget(
            self.calendarPage
        )

        self.setCentralWidget(
            self.pages
        )

    # =====================================================
    # CONNECTIONS
    # =====================================================

    def createConnections(self):

        # -------------------------
        # Login
        # -------------------------

        self.loginPage.accountCreationClicked.connect(
            self.showAccountCreation
        )

        self.loginPage.loginClicked.connect(
            self.login
        )

        # -------------------------
        # Account creation
        # -------------------------

        self.accountCreationPage.createAccountClicked.connect(
            self.createAccount
        )

        self.accountCreationPage.backToLoginClicked.connect(
            self.showLogin
        )

        # -------------------------
        # Planner list
        # -------------------------

        self.plannerListPage.createPlannerClicked.connect(
            self.createPlanner
        )

        self.plannerListPage.joinPlannerClicked.connect(
            self.joinPlanner
        )

        self.plannerListPage.plannerSelected.connect(
            self.openPlanner
        )

        self.plannerListPage.backToLoginClicked.connect(
            self.logout
        )

        # -------------------------
        # Calendar
        # -------------------------

        self.calendarPage.ingredientList.addIngredientClicked.connect(
            self.addIngredient
        )

        self.calendarPage.ingredientList.editIngredientClicked.connect(
            self.editIngredient
        )

        self.calendarPage.ingredientList.deleteIngredientClicked.connect(
            self.deleteIngredient
        )

        self.calendarPage.backToPlannerListClicked.connect(
            self.showPlannerList
        )

    # =====================================================
    # PAGES
    # =====================================================

    def showLogin(self):

        self.pages.setCurrentWidget(
            self.loginPage
        )

    def showAccountCreation(self):

        self.pages.setCurrentWidget(
            self.accountCreationPage
        )

    def showPlannerList(self):

        self.pages.setCurrentWidget(
            self.plannerListPage
        )

    # =====================================================
    # ACCOUNT CREATION
    # =====================================================

    def createAccount(self, userName, psw):

        try:

            response = requests.post(
                f"{self.apiUrl}/users",
                json={
                    "userName": userName,
                    "psw": psw
                },
                timeout=5
            )

            response.raise_for_status()

            user = response.json()

            print(
                "User created :",
                user
            )

            self.accountCreationPage.hideUserNameError()

            self.showLogin()

        except requests.HTTPError as error:

            if error.response.status_code == 409:

                self.accountCreationPage.showUserNameError()

            else:

                print(
                    "HTTP error :",
                    error
                )

        except requests.RequestException as error:

            print(
                "API error :",
                error
            )

    # =====================================================
    # LOGIN
    # =====================================================

    def login(self, userName, psw):

        try:

            response = requests.post(
                f"{self.apiUrl}/login",
                json={
                    "userName": userName,
                    "psw": psw
                },
                timeout=5
            )

            response.raise_for_status()

            user = response.json()

            self.userId = user["userId"]
            self.token = user["token"]

            self.settings.setValue(
                "token",
                self.token
            )

            # -------------------------
            # Planners de l'utilisateur
            # -------------------------

            response = requests.get(
                f"{self.apiUrl}/users/{self.userId}/planners",
                timeout=5
            )

            response.raise_for_status()

            planners = response.json()["planners"]

            self.plannerListPage.setPlanners(
                planners
            )

            # -------------------------
            # Tous les planners
            # -------------------------

            response = requests.get(
                f"{self.apiUrl}/planners",
                timeout=5
            )

            response.raise_for_status()

            allPlanners = response.json()

            self.plannerListPage.setAvailablePlanners(
                allPlanners
            )

            self.showPlannerList()

        except requests.RequestException as error:

            print(
                "Login error :",
                error
            )

    # =====================================================
    # CREATE PLANNER
    # =====================================================

    def createPlanner(self, name):

        try:

            response = requests.post(
                f"{self.apiUrl}/planners",
                json={
                    "name": name,
                    "userId": self.userId
                },
                timeout=5
            )

            response.raise_for_status()

            planner = response.json()

            print(
                "Planner created :",
                planner
            )

            self.plannerListPage.addPlanner(
                planner["plannerId"],
                planner["name"],
                planner["ownerName"]
            )

        except requests.HTTPError as error:

            print(
                "HTTP error :",
                error
            )

        except requests.RequestException as error:

            print(
                "API error :",
                error
            )

    # =====================================================
    # JOIN PLANNER
    # =====================================================

    def joinPlanner(self, plannerName, ownerId):

        try:

            response = requests.post(
                f"{self.apiUrl}/planners/join",
                json={
                    "name": plannerName,
                    "ownerId": ownerId,
                    "userId": self.userId
                },
                timeout=5
            )

            response.raise_for_status()

            planner = response.json()

            print(
                "Planner joined :",
                planner
            )

            self.plannerListPage.addPlanner(
                planner["plannerId"],
                planner["name"],
                planner["ownerName"]
            )

        except requests.HTTPError as error:

            print(
                "HTTP error :",
                error
            )

        except requests.RequestException as error:

            print(
                "API error :",
                error
            )

    # =====================================================
    # OPEN PLANNER
    # =====================================================

    def openPlanner(self, plannerId, plannerName):

        try:

            self.currentPlannerId = plannerId

            # -------------------------
            # Meals
            # -------------------------

            response = requests.get(
                f"{self.apiUrl}/meals",
                params={
                    "plannerId": plannerId
                },
                timeout=5
            )

            response.raise_for_status()

            meals = response.json()["meals"]

            # -------------------------
            # Ingredients
            # -------------------------

            response = requests.get(
                f"{self.apiUrl}/ingredients",
                params={
                    "plannerId": plannerId
                },
                timeout=5
            )

            response.raise_for_status()

            ingredients = response.json()["ingredients"]

            # -------------------------
            # Calendar
            # -------------------------

            self.calendarPage.setPlanner(
                plannerId
            )

            self.calendarPage.setTitle(
                plannerName
            )

            self.calendarPage.setSaveMealCallback(
                self.saveMeal
            )

            self.calendarPage.loadMeals(
                meals
            )

            self.calendarPage.setIngredients(
                ingredients
            )

            self.pages.setCurrentWidget(
                self.calendarPage
            )

        except requests.RequestException as error:

            print(
                "API error :",
                error
            )

    # =====================================================
    # SAVE MEAL
    # =====================================================

    def saveMeal(self, day, meal, content):

        if self.currentPlannerId is None:
            return

        try:

            response = requests.post(
                f"{self.apiUrl}/meals",
                json={
                    "plannerId": self.currentPlannerId,
                    "day": day,
                    "meal": meal,
                    "content": content
                },
                timeout=5
            )

            response.raise_for_status()

        except requests.HTTPError as error:

            print(
                "HTTP error :",
                error
            )

        except requests.RequestException as error:

            print(
                "API error :",
                error
            )

    # =====================================================
    # INGREDIENTS
    # =====================================================

    def addIngredient(self, content):

        try:

            response = requests.post(
                f"{self.apiUrl}/ingredients",
                json={
                    "plannerId": self.currentPlannerId,
                    "content": content
                },
                timeout=5
            )

            response.raise_for_status()

            ingredient = response.json()

            self.calendarPage.ingredientList.insertIngredient(
                ingredient["content"],
                ingredient["ingredientId"]
            )

        except requests.RequestException as error:

            print(
                "API error :",
                error
            )

    def editIngredient(self, item, content):

        try:

            response = requests.put(
                f"{self.apiUrl}/ingredients/{item.ingredientId}",
                json={
                    "content": content
                },
                timeout=5
            )

            response.raise_for_status()

            self.calendarPage.ingredientList.updateIngredient(
                item,
                content
            )

        except requests.RequestException as error:

            print(
                "API error :",
                error
            )

    def deleteIngredient(self, item, ingredientId):

        try:

            response = requests.delete(
                f"{self.apiUrl}/ingredients/{ingredientId}",
                timeout=5
            )

            response.raise_for_status()

            self.calendarPage.ingredientList.removeIngredient(
                item
            )

        except requests.RequestException as error:

            print(
                "API error :",
                error
            )

    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self):

        if self.token is not None:

            try:

                requests.delete(
                    f"{self.apiUrl}/session",
                    headers={
                        "Authorization": f"Bearer {self.token}"
                    },
                    timeout=5
                )

            except requests.RequestException as error:

                print(
                    "Logout server error :",
                    error
                )

        self.settings.remove(
            "token"
        )

        self.token = None
        self.userId = None
        self.currentPlannerId = None

        self.showLogin()

    # =====================================================
    # RESTORE SESSION
    # =====================================================

    def restoreSession(self):
        self.token = self.settings.value(
            "token"
        )

        if not self.token:
            return

        try:

            # -------------------------
            # Vérification du token
            # -------------------------

            response = requests.get(
                f"{self.apiUrl}/session",
                headers={
                    "Authorization": f"Bearer {self.token}"
                },
                timeout=5
            )

            if response.status_code == 401:

                print("Session token is invalid.")

                self.settings.remove(
                    "token"
                )

                self.token = None
                self.userId = None

                self.showLogin()

                return

            response.raise_for_status()

            session = response.json()

            self.userId = session["userId"]

            print(
                "Session restored :",
                self.userId
            )

            # -------------------------
            # Planners de l'utilisateur
            # -------------------------

            response = requests.get(
                f"{self.apiUrl}/users/{self.userId}/planners",
                timeout=5
            )

            response.raise_for_status()

            planners = response.json()["planners"]

            self.plannerListPage.setPlanners(
                planners
            )

            # -------------------------
            # Tous les planners
            # -------------------------

            response = requests.get(
                f"{self.apiUrl}/planners",
                timeout=5
            )

            response.raise_for_status()

            allPlanners = response.json()

            self.plannerListPage.setAvailablePlanners(
                allPlanners
            )

            self.pages.setCurrentWidget(
                self.plannerListPage
            )

        except requests.RequestException as error:

            print(
                "Session restore error :",
                error
            )