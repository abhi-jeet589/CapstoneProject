import pandas as pd
import logging

logger = logging.getLogger(__name__)


def parkingHistoryAggregation(parkingHistory,parkingLotDetails):
    logger.info("Aggregating parking history data")
    df_history = pd.DataFrame(parkingHistory)
    df_lot = pd.DataFrame(parkingLotDetails)
    df_merged = pd.merge(df_history,df_lot,left_on=['place_id'],right_on=['id'])
    df_merged.drop(columns=['place_id','id'],inplace=True,errors='ignore')
    return df_merged.to_json(orient='records')