import pandas as pd
import numpy as np

def parkingDetails(parkingDict):
    totalCoveredSlots, totalOccupiedSlots, totalVipSlots = 0,0,0
    for parkingLotName in parkingDict.keys():
        df_parkinglot = pd.DataFrame(parkingDict[parkingLotName])
        coveredSlots, occupiedSlots, vipSlots = df_parkinglot.aggregate(func=np.sum,axis=1)
        totalCoveredSlots += coveredSlots
        totalOccupiedSlots += occupiedSlots
        totalVipSlots += vipSlots
        del df_parkinglot
    
    return {
        'parkingLotList' : list(parkingDict.keys()),
        'totalCoveredSlots': totalCoveredSlots,
        'totalOccupiedSlots': totalOccupiedSlots,
        'totalVipSlots' : totalVipSlots,
        'parkingSlotDetails': parkingDict
    }
