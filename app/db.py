import sqlite3

CREATE_TABLE = "CREATE TABLE entities (name TEXT PRIMARY KEY, class TEXT)"
SELECT_WHERE = "SELECT * FROM entities WHERE name=?"
SELECT = "SELECT * FROM entities"
INSERT = "INSERT INTO entities VALUES (?, ?)"


class DatabaseConnection(object):

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename, check_same_thread=False)

    def create_schema(self):
        try:
            self.connection.execute(CREATE_TABLE)
        except sqlite3.OperationalError:
            print("Warning: 'entities' table already exists...")

    def get(self, name=None):
        cursor = (self.connection.execute(SELECT_WHERE, (name,))
                  if name is not None else self.connection.execute(SELECT))
        return cursor.fetchall()

    def add(self, name, cl):
        try:
            self.connection.execute(INSERT, (name, cl))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("Warning: '%s' is already in the database, ignoring..." % name)
            self.connection.rollback()