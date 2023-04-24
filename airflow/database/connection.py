import mysql.connector
import os
from dotenv import load_dotenv
import os

load_dotenv()

class SQLDatabase:
    def __init__(self):
        self.host = os.environ.get('SQL_HOSTNAME')
        self.user = os.environ.get('SQL_USERNAME')
        self.password = os.environ.get('SQL_PASSWORD')
        self.database = 'aircast'
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
                self.cursor = self.connection.cursor()
        except mysql.connector.Error as error:
            print(f"Failed to connect to MySQL database: {error}")

    def disconnect(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Disconnected from MySQL database")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except mysql.connector.Error as error:
            print(f"Failed to execute query: {error}")


instancesql = SQLDatabase()
instancesql.connect()
