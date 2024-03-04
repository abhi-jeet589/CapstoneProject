from .UtilLogger import UtilLogger
from yaml import safe_load


class UtilFetch:
    def __init__(self) -> None:
        try:
            self.logger = UtilLogger().getlogger(__name__)
            with open('sql.yml','r') as fileptr:
                self.logger.info("Fetching SQL file")
                self.sql = safe_load(fileptr)
        except Exception as err:
            self.logger.exception(err)
            raise Exception(err)
    
    def select_sql(self,db,table,action):
        try:
            self.logger.debug(f"Performing {action} operation on: {db}:{table}")
            self.logger.debug(self.sql[db][table][action])
            return self.sql[db][table][action]
        except Exception as err:
            self.logger.exception(err)

    def select_sql_one_condition(self,db,table,action,condition):
        try:
            self.logger.debug(f"Performing {action} operation on: {db}:{table}")
            sql = self.sql[db][table][action]
            processed_condition = self.append_none_tuple(condition)
            self.logger.debug(sql.format(processed_condition))
            return sql.format(processed_condition)
        except Exception as err:
            self.logger.exception(err)

    def select_sql_two_condition(self,db,table,action,condition1,condition2):
        try:
            self.logger.debug(f"Performing {action} operation on: {db}:{table}")
            sql = self.sql[db][table][action]
            processed_condition2 = self.append_none_tuple(condition2)
            self.logger.debug(sql.format(condition1,processed_condition2))
            return sql.format(condition1,processed_condition2)
        except Exception as err:
            self.logger.exception(err)

    def select_sql_none_tuple_condition(self,db,table,action,condition):
        try:
            self.logger.debug(f"Performing {action} operation on: {db}:{table}")
            sql = self.sql[db][table][action]
            self.logger.debug(sql.format(condition))
            return sql.format(condition)
        except Exception as err:
            self.logger.exception(err)

    def append_none_tuple(self,condition):
        try:
            condition = list(condition)
            if len(condition) == 1:
                condition.append('None')
            return tuple(condition)
        except Exception as err:
            self.logger.exception(err)