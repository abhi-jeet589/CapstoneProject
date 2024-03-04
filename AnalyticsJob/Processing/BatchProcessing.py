from Utils.UtilLogger import UtilLogger
from Utils.UtilFetch import UtilFetch
from uuid import uuid4
from datetime import datetime
import pandas as pd
from ast import literal_eval


class BatchProcessing:
    def __init__(self,cursor,db) -> None:
        self.logger = UtilLogger().getlogger(__name__)
        self.BATCH_ID = int(str(uuid4().int)[:16])
        self.util_fetch = UtilFetch()
        self._db = db
        self._cursor = cursor
        self.batch_records = 0

    def enable_batch_processing(self):
        try:
            self.logger.info("Starting batch processing")
            condition = (self.BATCH_ID,datetime.today().strftime('%Y-%m-%d'),'Running')
            create_batch_sql = self.util_fetch.select_sql_one_condition('Analytics','BatchJob','Create',condition)
            self._cursor.execute(create_batch_sql)
            self._db.commit()
            self.fetch_processing_records()
        except Exception as err:
            self.logger.exception(err)

    def fetch_processing_records(self):
        try:
            self.logger.info("Fetching processing records")
            get_processing_records = self.util_fetch.select_sql('Analytics','BatchRecords','Read')
            self._cursor.execute(get_processing_records)
            columns = self._cursor.description
            data = [{columns[index][0]: column for index, column in enumerate(value)} for value in self._cursor.fetchall()]
            if len(data) > 0:
                self.df_processing_records = pd.DataFrame(data)
                for record_id,upstream_object,downstream_object,record in list(zip(self.df_processing_records['id'].values,self.df_processing_records['upstream_object'].values,self.df_processing_records['downstream_object'].values,self.df_processing_records['record'].values)):
                    try:
                        self.batch_records+=1
                        self.logger.info(f"Processing {upstream_object} object")
                        self.process_records(record_id,upstream_object,downstream_object,record)
                    except Exception as err:
                        self.batch_records-=1
                        self.logger.exception(err)
                        self.update_record_status("Failed",record_id)
            self.update_batch_status("Success",self.batch_records)
        except Exception as err:
            self.logger.exception(err)
            self.update_batch_status("Failed",self.batch_records)

    def process_records(self,record_id,upstream_object,downstream_object,record):
        try:
            date_condition = [datetime.today().strftime('%Y-%m-%d')]
            get_date_specific_analytics = self.util_fetch.select_sql('Analytics',upstream_object.capitalize(),'SpecificAnalytics')
            self._cursor.execute(get_date_specific_analytics,date_condition)
            columns = self._cursor.description
            data = [{columns[index][0]: column for index, column in enumerate(value)} for value in self._cursor.fetchall()]
            record = literal_eval(record)

            if len(data) > 0:
                self.logger.info("Current date analytics exist")
                df_date_specific_analytics = pd.DataFrame(data)
                final_value = df_date_specific_analytics[df_date_specific_analytics.columns[0]].values[0] + record['value']
                self.logger.info(f"Updating {upstream_object} analytics")
                update_downstream_object = self.util_fetch.select_sql_none_tuple_condition('Analytics',upstream_object.capitalize(),'UpdateAnalytics',final_value)
                self._cursor.execute(update_downstream_object,date_condition)
                self._db.commit()
        
            else:
                self.logger.info(f"Inserting {upstream_object} analytics")
                insert_condition = (record['current_date'],record['value'])
                insert_downstream_object = self.util_fetch.select_sql_one_condition('Analytics',upstream_object.capitalize(),'DownstreamInsert',insert_condition)
                self._cursor.execute(insert_downstream_object)
                self._db.commit()
            
            self.update_record_status("Success",record_id)
        except Exception as err:
            self.logger.exception(err)

    def update_record_status(self,status:str,record_id):
        try:
            id_list = tuple([record_id])
            update_record_sql = self.util_fetch.select_sql_one_condition('Analytics','BatchRecords','Update',id_list)
            self._cursor.execute(update_record_sql,(status,self.BATCH_ID))
            self._db.commit()
        except Exception as err:
            self.logger.exception(err)

    def update_batch_status(self,status:str,no_of_records):
        try:
            self.logger.info(f"Updating {status} status for job: {self.BATCH_ID}")
            update_batch_status_sql = self.util_fetch.select_sql('Analytics','BatchJob','UpdateEndTime')
            self._cursor.execute(update_batch_status_sql,(datetime.today().strftime('%Y-%m-%d'),status,no_of_records,self.BATCH_ID))
            self._db.commit()
        except Exception as err:
            self.logger.exception(err)