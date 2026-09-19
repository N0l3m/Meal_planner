import sqlite3


class Database:

    def __init__(self, databaseName="mealPlanner.db"):

        self.connection = sqlite3.connect(
            databaseName
        )

        self.createTables()

    def createTables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY,
                day TEXT NOT NULL,
                meal TEXT NOT NULL,
                content TEXT NOT NULL DEFAULT '',
                UNIQUE(day, meal)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                position INTEGER NOT NULL
            )
        """)

        self.connection.commit()

    # -------------------------
    # Ingredients
    # -------------------------

    def addIngredient(self, text):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT MAX(position)
            FROM ingredients
        """)

        result = cursor.fetchone()

        if result[0] is None:
            position = 0
        else:
            position = result[0] + 1

        cursor.execute("""
            INSERT INTO ingredients
            (content, position)
            VALUES (?, ?)
        """, (text, position))

        self.connection.commit()

    def getIngredients(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT id, content, position
            FROM ingredients
            ORDER BY position
        """)

        return cursor.fetchall()

    def editIngredient(self, ingredientId, text):

        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE ingredients
            SET content = ?
            WHERE id = ?
        """, (text, ingredientId))

        self.connection.commit()

    def deleteIngredient(self, ingredientId):

        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM ingredients
            WHERE id = ?
        """, (ingredientId,))

        self.connection.commit()

    # -------------------------
    # Menus
    # -------------------------

    def getMeal(self, day, meal):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT content
            FROM meals
            WHERE day = ? AND meal = ?
        """, (day, meal))

        result = cursor.fetchone()

        if result is None:
            return ""

        return result[0]

    def setMeal(self, day, meal, content):

        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE meals
            SET content = ?
            WHERE day = ? AND meal = ?
        """, (content, day, meal))

        self.connection.commit()

    def getMeals(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT day, meal, content
            FROM meals
            ORDER BY id
        """)

        return cursor.fetchall()

    def initializeMeals(self, days, meals):
        cursor = self.connection.cursor()

        for day in days:
            for meal in meals:
                cursor.execute("""
                    INSERT OR IGNORE INTO meals
                    (day, meal, content)
                    VALUES (?, ?, '')
                """, (day, meal))

        self.connection.commit()

    def close(self):

        self.connection.close()
