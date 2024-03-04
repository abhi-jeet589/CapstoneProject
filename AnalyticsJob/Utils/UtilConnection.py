from .UtilLogger import UtilLogger
import mysql.connector as mysqlconnect
from os import environ
import json

class UtilConnection:
    def __init__(self):
        try:
            self.logger = UtilLogger().getlogger(__name__)
            self.logger.info("Using config.json file")
            with open('config.json') as fileptr:
                config = json.load(fileptr)
            self._dbname = config['DATABASE']['DBNAME']
            self._user = config['DATABASE']['DBUSER']
            self._password = config['DATABASE']['DBPASSWORD']
            self._host = config['DATABASE']['DBHOST']
            self._port = int(config['DATABASE']['DBPORT'])
            self.logger.debug(f"HOST: {self._host} PORT: {self._port} PASSWORD: {self._password} DBNAME: {self._dbname} DBUSER: {self._user}")
        except Exception as err:
            self.logger.exception(err)
            self.logger.info("Using environment variables to connect to DB")
            self._dbname = environ.get("DBNAME","")
            self._user = environ.get("DBUSER","")
            self._password = environ.get("DBPASSWORD",'')
            self._host = environ.get("DBHOST","localhost")
            self._port = environ.get("DBPORT",3306)
        
            
    def connectToDb(self):
        try:
            self.logger.info("Connecting to MYSQL database at {}".format(self._host))
            self._dbConnection = mysqlconnect.connect(user=self._user,password=self._password,host=self._host,port=self._port,database=self._dbname)
            return self._dbConnection
        except mysqlconnect.Error as err:
            self.logger.exception(err)
            raise Exception(err)
            
    def create_cursor(self):
        try:
            if self._dbConnection.is_connected() == True:
                return self._dbConnection.cursor()
        except Exception as err:
            self.logger.exception("No connection to database")
            raise Exception(err)
            
