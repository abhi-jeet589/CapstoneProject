import logging

class UtilLogger:
    def __init__(self,name):
        self._logger = logging.getLogger(name)

    def getlogger(self) -> logging.Logger:
        return self._logger