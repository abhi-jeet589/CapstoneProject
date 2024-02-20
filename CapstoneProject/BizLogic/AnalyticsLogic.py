import pandas as pd
from Utils.UtilLogger import UtilLogger
import logging

def parkingDetails(parkingDict):
    logger = UtilLogger(__name__).getlogger()
    logger.addHandler(logging.StreamHandler)
    logger.info("Aggregating data")
    parkingLotDetails = {}
    for parkingLotName in parkingDict.keys():
        totalCoveredSlots, totalOccupiedSlots, totalVipSlots = 0,0,0
        df_parkinglot = pd.DataFrame(parkingDict[parkingLotName])
        coveredSlots, occupiedSlots, vipSlots = df_parkinglot.aggregate(func="sum",axis=1)
        totalCoveredSlots += coveredSlots
        totalOccupiedSlots += occupiedSlots
        totalVipSlots += vipSlots
        del df_parkinglot
        parkingLotDetails[parkingLotName] = {
        'totalCoveredSlots': totalCoveredSlots,
        'totalOccupiedSlots': totalOccupiedSlots,
        'totalVipSlots' : totalVipSlots,
        'parkingSlotDetails': parkingDict[parkingLotName]
    }
    
    return parkingLotDetails