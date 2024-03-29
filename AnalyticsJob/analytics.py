from Utils.UtilConnection import UtilConnection as UtilConnect
from Utils.UtilLogger import UtilLogger
from BizLogic import UserLogic, RevenueLogic
from Processing.BatchProcessing import BatchProcessing
import logging

if __name__ == '__main__':
    ##Set logging config
    logging.basicConfig(format='%(asctime)s - [%(name)s] - [%(levelname)s] - %(message)s',level=logging.DEBUG)

    ##Instantiate all required modules
    utilConnect = UtilConnect()
    db = utilConnect.connectToDb()
    logger = UtilLogger().getlogger(__name__)
    cursor = utilConnect.create_cursor()

    ##Object level processing
    userLogic = UserLogic.UserLogic(cursor,db)
    userLogic.manage_user_data()

    revenueLogic = RevenueLogic.RevenueLogic(cursor,db)
    revenueLogic.manage_revenue_data()

    ##Batch job processing
    batchProcessing = BatchProcessing(cursor=cursor,db=db)
    batchProcessing.enable_batch_processing()