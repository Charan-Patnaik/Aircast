#%%
import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

#%%
class SQLDatabase:
    def __init__(self):
        self.host = os.environ.get('SQL_HOSTNAME')
        self.user = os.environ.get('SQL_USERNAME')
        self.password = os.environ.get('SQL_PASSWORD')
        self.database = 'aircast'
        self.connection = None
        self.cursor = None
        print(self.host, self.user,  self.password, self.database)

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
            print(f"Failed to connect to SQL database: {error}")

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

    


#%%
instancesql = SQLDatabase()
instancesql.connect()
#%%
table_name = 'StationsData'
csv_file_path = '/Users/varshahindupur/Desktop/GitHub/Aircast/airflow/models/data/AirQualityData_Modified.csv'
# write the DataFrame to the MySQL database using the to_sql() method
df = pd.read_csv(csv_file_path, sep=',')
# instancesql.load_data_from_csv_into_db(df, table_name)

instancesql.disconnect()
