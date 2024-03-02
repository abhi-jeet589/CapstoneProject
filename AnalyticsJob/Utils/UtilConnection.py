import mysql.connector as mysqlconnect
from os import environ
import json


class UtilConnection:
    def __init__(self):
        try:
            print("Using environment variables to connect to DB")
            self._dbname = environ.get("DBNAME","analytics")
            self._user = environ.get("DBUSER","capstone_user")
            self._password = environ.get("DBPASSWORD",'password')
            self._host = environ.get("DBHOST","localhost")
            self._port = environ.get("DBPORT",3306)
        except Exception as err:
            print(err)
            try:
                print("Using config.json file")
                with open('./../config.json') as fileptr:
                    config = json.load(fileptr)
                self._dbname = config['DATABASE']['DBNAME']
                self._user = config['DATABASE']['DBUSER']
                self._password = config['DATABASE']['DBPASSWORD']
                self._host = config['DATABASE']['DBHOST']
                self._port = int(config['DATABASE']['DBPORT'])
            except FileNotFoundError as err:
                raise FileNotFoundError()
            
    def connectToDb(self):
        try:
            self._dbConnection = mysqlconnect.connect(user=self._user,password=self._password,host=self._host,port=self._port,database=self._dbname)
        except mysqlconnect.Error as err:
            raise Exception(err)
        
    def getDbConnection(self):
        if self._dbConnection.is_connected() == True:
            return self._dbConnection
        else:
            print("No connection to database")
            
        

