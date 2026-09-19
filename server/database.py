import os
import sqlite3
import secrets


class Database:

    def __init__(self, databaseName="server.db"):

        databasePath = os.getenv(
            "DB_PATH",
            databaseName
        )

        self.connection = sqlite3.connect(
            databasePath,
            check_same_thread=False
        )

        self.connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        self.createTables()

    def createTables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                userName TEXT NOT NULL UNIQUE,
                psw TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS planners (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                ownerId INTEGER NOT NULL,
                UNIQUE(name, ownerId),
                FOREIGN KEY (ownerId) REFERENCES users(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS planner_members (
                userId INTEGER NOT NULL,
                plannerId INTEGER NOT NULL,
                role TEXT NOT NULL DEFAULT 'member',

                PRIMARY KEY (userId, plannerId),

                FOREIGN KEY (userId)
                    REFERENCES users(id),

                FOREIGN KEY (plannerId)
                    REFERENCES planners(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY,
                plannerId INTEGER NOT NULL,
                day TEXT NOT NULL,
                meal TEXT NOT NULL,
                content TEXT NOT NULL DEFAULT '',

                UNIQUE(plannerId, day, meal),

                FOREIGN KEY (plannerId)
                    REFERENCES planners(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY,
                plannerId INTEGER NOT NULL,
                content TEXT NOT NULL COLLATE NOCASE,
                position INTEGER NOT NULL,

                UNIQUE(plannerId, content),

                FOREIGN KEY (plannerId)
                    REFERENCES planners(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                userId INTEGER NOT NULL,

                FOREIGN KEY (userId)
                    REFERENCES users(id)
            )
        """)

        self.connection.commit()

    def getMeals(self, plannerId):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT day, meal, content
            FROM meals
            WHERE plannerId = ?
            ORDER BY id
        """, (plannerId,))

        return cursor.fetchall()

    def setMeal(self, plannerId, day, meal, content):

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO meals (plannerId, day, meal, content)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(plannerId, day, meal)
            DO UPDATE SET content = excluded.content
        """, (plannerId, day, meal, content))

        self.connection.commit()

    def getUserInfos(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT id, userName, psw
            FROM users
            ORDER BY id
        """)

        return cursor.fetchall()

    def setUserInfos(self, userName, psw):

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO users (userName, psw)
            VALUES (?, ?)
        """, (userName, psw))

        self.connection.commit()

        return cursor.lastrowid

    def getPlannerInfos(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT
                p.id,
                p.name,
                p.ownerId,
                u.userName
            FROM planners p
            JOIN users u
                ON u.id = p.ownerId
            ORDER BY p.id
        """)

        return cursor.fetchall()

    def setPlannerInfos(self, name, ownerId):
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO planners (name, ownerId)
            VALUES (?, ?)
        """, (name, ownerId))

        self.connection.commit()

        return cursor.lastrowid

    def getUserPlanners(self, userId):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT
                p.id,
                p.name,
                p.ownerId,
                u.userName
            FROM planners p
            JOIN planner_members pm
                ON pm.plannerId = p.id
            JOIN users u
                ON u.id = p.ownerId
            WHERE pm.userId = ?
            ORDER BY p.name
        """, (userId,))

        return cursor.fetchall()

    def getPlannerMembers(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT userId, plannerId, role
            FROM planner_members
        """)

        return cursor.fetchall()

    def addPlannerMember(self, userId, plannerId, role="member"):

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO planner_members (userId, plannerId, role)
            VALUES (?, ?, ?)
        """, (userId, plannerId, role))

        self.connection.commit()

    def checkUser(self, userName, psw):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT id
            FROM users
            WHERE userName = ?
            AND psw = ?
        """, (userName, psw))

        result = cursor.fetchone()

        if result is None:
            return None

        return result[0]

    def createPlanner(self, name, userId):
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO planners (name, ownerId)
            VALUES (?, ?)
        """, (name, userId))

        plannerId = cursor.lastrowid

        cursor.execute("""
            INSERT INTO planner_members (
                userId,
                plannerId,
                role
            )
            VALUES (?, ?, ?)
        """, (
            userId,
            plannerId,
            "owner"
        ))

        self.connection.commit()

        return plannerId

    def joinPlanner(self, name, ownerId, userId):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT id, name
            FROM planners
            WHERE name = ?
            AND ownerId = ?
        """, (name, ownerId))

        planner = cursor.fetchone()

        if planner is None:
            return None

        plannerId = planner[0]
        plannerName = planner[1]

        cursor.execute("""
            INSERT INTO planner_members (userId, plannerId, role)
            VALUES (?, ?, 'member')
        """, (userId, plannerId))

        self.connection.commit()

        return plannerId, plannerName

    def getIngredients(self, plannerId):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT id, content, position
            FROM ingredients
            WHERE plannerId = ?
            ORDER BY position, id
        """, (plannerId,))

        return cursor.fetchall()


    def addIngredient(self, plannerId, content):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT COALESCE(MAX(position), -1) + 1
            FROM ingredients
            WHERE plannerId = ?
        """, (plannerId,))

        position = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO ingredients (
                plannerId,
                content,
                position
            )
            VALUES (?, ?, ?)
        """, (
            plannerId,
            content,
            position
        ))

        self.connection.commit()

        return cursor.lastrowid


    def editIngredient(self, ingredientId, content):
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE ingredients
            SET content = ?
            WHERE id = ?
        """, (
            content,
            ingredientId
        ))

        self.connection.commit()


    def deleteIngredient(self, ingredientId):
        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM ingredients
            WHERE id = ?
        """, (ingredientId,))

        self.connection.commit()

    def createSession(self, userId):
        token = secrets.token_urlsafe(32)

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO sessions (token, userId)
            VALUES (?, ?)
        """, (token, userId))

        self.connection.commit()

        return token

    def getUserFromToken(self, token):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT userId
            FROM sessions
            WHERE token = ?
        """, (token,))

        result = cursor.fetchone()

        if result is None:
            return None

        return result[0]

    def deleteSession(self, token):
        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM sessions
            WHERE token = ?
        """, (token,))

        self.connection.commit()