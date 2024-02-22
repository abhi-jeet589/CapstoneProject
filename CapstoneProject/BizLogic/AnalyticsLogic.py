import pandas as pd
import logging

def parkingDetails(parkingDict):
    logger = logging.getLogger(__name__)
    logger.info("Aggregating data")
    parkingLotDetails = {}
    for parkingLotName in parkingDict.keys():
        totalCoveredSlots, totalOccupiedSlots, totalVipSlots = 0,0,0
        df_parkinglot = pd.DataFrame(parkingDict[parkingLotName])
        coveredSlots, occupiedSlots, vipSlots = df_parkinglot.aggregate(func="sum",axis=1)
        totalCoveredSlots += coveredSlots
        totalOccupiedSlots += occupiedSlots
        totalVipSlots += vipSlots
        parkingLotDetails[parkingLotName] = {
        'totalParkingSlots': len(df_parkinglot) - 1,
        'totalOccupiedSlots': totalOccupiedSlots,
        'totalAvailableSlots': len(df_parkinglot) - 1 - totalOccupiedSlots,
        'totalCoveredSlots': totalCoveredSlots,
        'totalVipSlots' : totalVipSlots,
        'parkingSlotDetails': parkingDict[parkingLotName]
    }
        del df_parkinglot
        
    return parkingLotDetails