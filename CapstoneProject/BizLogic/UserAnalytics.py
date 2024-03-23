import pandas as pd
import logging
import json

month_dict = {1: 'January',2 : 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

def userDetails(data):
    logger = logging.getLogger(__name__)
    logger.info("Aggregating monthly user data")
    if len(data) > 0:
        json_str = json.dumps(data)
        dict_data = json.loads(json_str)
        df = pd.DataFrame(dict_data)
        response = {}
        df['date_processed'] = pd.to_datetime(df['date_processed'])
        df['date_processed_month'] = df['date_processed'].dt.month
        result = df.groupby(df['date_processed_month'])['no_of_users'].sum()
        for month_no, month_name in month_dict.items():
            response[month_name] = result.get(month_no,0)
    return response