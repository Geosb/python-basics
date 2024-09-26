import mysql.connector
import configparser


class MySQLConnector:
    def __init__(self, config_file='baoso.txt'):
        self.config = self._read_config(config_file)
        self.connection = None

    def _read_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config['mysql']

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database']
            )
            print("Connected to MySQL database successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")
