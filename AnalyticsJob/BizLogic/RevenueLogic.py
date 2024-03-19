import pandas as pd
from Utils.UtilLogger import UtilLogger
from Utils.UtilFetch import UtilFetch
from datetime import datetime

class RevenueLogic:
    def __init__(self,cursor,db) -> None:
        self.logger = UtilLogger().getlogger(__name__)
        self.utilFetch = UtilFetch()
        self.UPSTREAM_OBJECT = 'booking_sessions'
        self.DOWNSTREAM_OBJECT = 'revenue_analytics'
        self.PROCESSED = 'Pending'
        self._cursor = cursor
        self._db = db

    def manage_revenue_data(self):
        try:
            get_user_sql = self.utilFetch.select_sql('Analytics','Booking_sessions','UpstreamFetch')
            self._cursor.execute(get_user_sql)
            columns = self._cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in self._cursor.fetchall()]
            if len(result) > 0:
                self.logger.info(f"Fetched {len(result)} rows")
                self.prepare_data(result)
        except Exception as err:
            self.logger.exception(err)

    def prepare_data(self,user_data:list):
        try:
            self.logger.info("Preparing data to send for further processing")
            df_revenue = pd.DataFrame(user_data)
            total_revenue = df_revenue['calculated_bill'].aggregate(func="sum")
            current_date = datetime.today().strftime('%Y-%m-%d')
            self.send_data_for_processing({'current_date' : current_date, 'value': total_revenue},df_revenue['session_id'].unique())
        except Exception as err:
            self.logger.exception(err)

    def send_data_for_processing(self,data:dict,id_list):
        try:
            self.logger.info("Sending data for batch processing")
            condition = (self.UPSTREAM_OBJECT,self.DOWNSTREAM_OBJECT,f'{data}',self.PROCESSED)
            batch_processing_sql = self.utilFetch.select_sql('Analytics','BatchRecords','Create')
            self._cursor.execute(batch_processing_sql,condition)
            self._db.commit()
            update_user_sql = self.utilFetch.select_sql_one_condition('Analytics','Booking_sessions','Update',list(id_list))
            self._cursor.execute(update_user_sql)
            self._db.commit()
        except Exception as err:
            self.logger.exception(err)