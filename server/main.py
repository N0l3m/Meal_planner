from fastapi import FastAPI, HTTPException, Header
from database import Database
from pydantic import BaseModel

import sqlite3


app = FastAPI()

database = Database()

print(database)


# =====================================================
# MODELS
# =====================================================

class Meal(BaseModel):
    plannerId: int
    day: str
    meal: str
    content: str


class User(BaseModel):
    userName: str
    psw: str


class Planner(BaseModel):
    name: str
    userId: int


class PlannerJoin(BaseModel):
    name: str
    ownerId: int
    userId: int


class PlannerMember(BaseModel):
    userId: int
    plannerId: int
    role: str = "member"


class Login(BaseModel):
    userName: str
    psw: str


class Ingredient(BaseModel):
    plannerId: int
    content: str


class IngredientUpdate(BaseModel):
    content: str


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():

    return {
        "message": "Meal Planner Server"
    }


# =====================================================
# MEALS
# =====================================================

@app.get("/meals")
def get_meals(plannerId: int):

    meals = database.getMeals(
        plannerId
    )

    return {
        "meals": meals
    }


@app.post("/meals")
def create_meal(meal: Meal):

    database.setMeal(
        meal.plannerId,
        meal.day,
        meal.meal,
        meal.content
    )

    return {
        "message": "Meal saved"
    }


# =====================================================
# USERS
# =====================================================

@app.get("/users")
def get_userInfos():

    users = database.getUserInfos()

    return {
        "user": users
    }


@app.post("/users")
def set_userInfos(user: User):

    if len(user.psw) < 6:

        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 6 characters"
        )

    try:

        userId = database.setUserInfos(
            user.userName,
            user.psw
        )

        return {
            "userId": userId,
            "userName": user.userName
        }

    except sqlite3.IntegrityError:

        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )


# =====================================================
# PLANNERS
# =====================================================

@app.get("/planners")
def get_plannerInfos():

    planners = database.getPlannerInfos()

    return [
        {
            "plannerId": planner[0],
            "name": planner[1],
            "ownerId": planner[2],
            "ownerName": planner[3]
        }
        for planner in planners
    ]


@app.post("/planners")
def set_plannerInfos(planner: Planner):

    try:

        plannerId = database.createPlanner(
            planner.name,
            planner.userId
        )

        cursor = database.connection.cursor()

        cursor.execute("""
            SELECT userName
            FROM users
            WHERE id = ?
        """, (planner.userId,))

        result = cursor.fetchone()

        if result is None:

            raise HTTPException(
                status_code=404,
                detail="Owner not found"
            )

        ownerName = result[0]

        return {
            "plannerId": plannerId,
            "name": planner.name,
            "ownerId": planner.userId,
            "ownerName": ownerName
        }

    except sqlite3.IntegrityError:

        raise HTTPException(
            status_code=409,
            detail="Planner already exists for this owner"
        )


# =====================================================
# PLANNER MEMBERS
# =====================================================

@app.get("/plannerMembers")
def get_planner_members():

    members = database.getPlannerMembers()

    return {
        "members": members
    }


@app.post("/plannerMembers")
def add_planner_member(member: PlannerMember):

    database.addPlannerMember(
        member.userId,
        member.plannerId,
        member.role
    )

    return {
        "message": "member added"
    }


# =====================================================
# USER PLANNERS
# =====================================================

@app.get("/users/{userId}/planners")
def get_user_planners(userId: int):

    planners = database.getUserPlanners(
        userId
    )

    return {
        "planners": [
            {
                "plannerId": planner[0],
                "name": planner[1],
                "ownerId": planner[2],
                "ownerName": planner[3]
            }
            for planner in planners
        ]
    }


# =====================================================
# JOIN PLANNER
# =====================================================

@app.post("/planners/join")
def join_planner(planner: PlannerJoin):

    try:

        result = database.joinPlanner(
            planner.name,
            planner.ownerId,
            planner.userId
        )

        if result is None:

            raise HTTPException(
                status_code=404,
                detail="Planner not found"
            )

        plannerId, plannerName = result

        cursor = database.connection.cursor()

        cursor.execute("""
            SELECT userName
            FROM users
            WHERE id = ?
        """, (planner.ownerId,))

        owner = cursor.fetchone()

        if owner is None:

            raise HTTPException(
                status_code=404,
                detail="Owner not found"
            )

        ownerName = owner[0]

        return {
            "plannerId": plannerId,
            "name": plannerName,
            "ownerId": planner.ownerId,
            "ownerName": ownerName
        }

    except sqlite3.IntegrityError:

        raise HTTPException(
            status_code=409,
            detail="User already belongs to this planner"
        )


# =====================================================
# LOGIN
# =====================================================

@app.post("/login")
def login(user: Login):

    userId = database.checkUser(
        user.userName,
        user.psw
    )

    if userId is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = database.createSession(
        userId
    )

    return {
        "userId": userId,
        "userName": user.userName,
        "token": token
    }


# =====================================================
# INGREDIENTS
# =====================================================

@app.get("/ingredients")
def get_ingredients(plannerId: int):

    ingredients = database.getIngredients(
        plannerId
    )

    return {
        "ingredients": ingredients
    }


@app.post("/ingredients")
def create_ingredient(ingredient: Ingredient):

    try:

        ingredientId = database.addIngredient(
            ingredient.plannerId,
            ingredient.content
        )

        return {
            "ingredientId": ingredientId,
            "content": ingredient.content
        }

    except sqlite3.IntegrityError:

        raise HTTPException(
            status_code=409,
            detail="Ingredient already exists"
        )


@app.put("/ingredients/{ingredientId}")
def edit_ingredient(
    ingredientId: int,
    ingredient: IngredientUpdate
):

    try:

        database.editIngredient(
            ingredientId,
            ingredient.content
        )

        return {
            "message": "Ingredient updated"
        }

    except sqlite3.IntegrityError:

        raise HTTPException(
            status_code=409,
            detail="Ingredient already exists"
        )


@app.delete("/ingredients/{ingredientId}")
def delete_ingredient(ingredientId: int):

    database.deleteIngredient(
        ingredientId
    )

    return {
        "message": "Ingredient deleted"
    }


# =====================================================
# SESSION
# =====================================================

@app.get("/session")
def restore_session(
    authorization: str | None = Header(default=None)
):

    # -------------------------
    # Vérification du header
    # -------------------------

    if authorization is None:

        raise HTTPException(
            status_code=401,
            detail="Missing token"
        )

    if not authorization.startswith("Bearer "):

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    # -------------------------
    # Récupération du token
    # -------------------------

    token = authorization[7:]

    # -------------------------
    # Recherche du user
    # -------------------------

    userId = database.getUserFromToken(
        token
    )

    if userId is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return {
        "userId": userId
    }


@app.delete("/session")
def delete_session(
    authorization: str | None = Header(default=None)
):

    if authorization is None:

        raise HTTPException(
            status_code=401,
            detail="Missing token"
        )

    if not authorization.startswith("Bearer "):

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    token = authorization[7:]

    database.deleteSession(
        token
    )

    return {
        "message": "Logged out"
    }
