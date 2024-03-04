import logging

class UtilLogger:
    def getlogger(self,name) -> logging.Logger:
        return logging.getLogger(name)