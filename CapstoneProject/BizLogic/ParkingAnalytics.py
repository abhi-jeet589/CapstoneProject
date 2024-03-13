import pandas as pd
import numpy as np
import logging

def parkingDetails(parkingDict):
    logger = logging.getLogger(__name__)
    logger.info("Aggregating data")
    parkingLotDetails = {}
    columnIgnoreList = {'Gate','Settings','Status'}
    for parkingLotName in parkingDict.keys():
        totalCoveredSlots, totalOccupiedSlots, totalVipSlots = 0,0,0
        df_parkinglot = pd.DataFrame(parkingDict[parkingLotName])
        df_parkinglot = df_parkinglot.drop(columns=columnIgnoreList,errors='ignore')
        coveredSlots = df_parkinglot.loc['covered'].aggregate(func="sum",axis=0)
        occupiedSlots = df_parkinglot.loc['occupied'].aggregate(func="sum",axis=0)
        vipSlots = df_parkinglot.loc['vip'].aggregate(func="sum",axis=0)
        totalCoveredSlots += coveredSlots
        totalOccupiedSlots += occupiedSlots
        totalVipSlots += vipSlots
        for col in columnIgnoreList:
            parkingDict[parkingLotName].pop(col,None)
        parkingLotDetails[parkingLotName] = {
        'totalParkingSlots': len(df_parkinglot.columns),
        'totalOccupiedSlots': totalOccupiedSlots,
        'totalAvailableSlots': len(df_parkinglot.columns) - totalOccupiedSlots,
        'totalCoveredSlots': totalCoveredSlots,
        'totalVipSlots' : totalVipSlots,
        'parkingSlotDetails': parkingDict[parkingLotName]
    }
        del df_parkinglot
        
    return parkingLotDetails