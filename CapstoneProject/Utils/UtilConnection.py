import pyrebase as pyre
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class DBConnect:
    def __init__(self):
        self._firebaseConfig = {
            "apiKey": getenv("APIKEY"),
            "authDomain": getenv("AUTHDOMAIN"),
            "databaseURL": getenv("DATABASEURL"),
            "projectId": getenv("PROJECTID"),
            "storageBucket" : getenv("STORAGEBUCKET"),
            "messagingSenderId" : getenv("MESSAGINGSENDERID"),
            "appId": getenv("APPID"),
            "measurementId": getenv("MEASUREMENTID")
        }
    
    def connectDb(self):
        self._firebase = pyre.initialize_app(self._firebaseConfig)
        self._db=self._firebase.database()

    def getDb(self):
        return self._db