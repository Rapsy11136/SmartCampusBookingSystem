import sqlite3
from config import DATABASE_NAME


class Database:

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()

    def execute(self, query, values=()):
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def fetchone(self, query, values=()):
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    def fetchall(self, query, values=()):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()