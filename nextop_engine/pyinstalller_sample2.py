
# coding: utf-8

import os, sys
path_name= os.getcwd()
sys.path.append(path_name)
print(path_name)

from _element import feature_control as ft_c
from _element.data_control import Data, DataRestruction, DataAddition
from _element import varr
from _element import calculations as calc
from _element.result_control import Result

from _alg.prophet import Prophet_timeseries
from _alg.arima import Arima_timeseries

from _evaluation.cross_validation import Cross_Validation
from _evaluation import compare

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture


INPUT_FILENAME= 'KPP일별입고(13_17)_daily_obj.xlsx'
df_raw= ft_c.xlsx_opener(INPUT_FILENAME, path_name+varr.DF_DIR)
data= Data()
data.setRawData(df_raw)

restruct= DataRestruction(data)
restruct.selectSpecificY(['y_sum'])
df_commit= restruct.commitRestructedData()
df_temp= ft_c.xlsx_opener('temp_data_merged.xlsx', path_name+varr.TEMP_DATA_DIR)
addition= DataAddition(data)
addition.addXData(df_temp)
df_commit= addition.commitAddedData()

restruct= DataRestruction(data)
restruct.addRegion(7, 'weekdayRegion', start_num= 3)
condition_only_sun= {
    'weekday': (0,1,2,3,4,),
    'sat': (5, ),
    'sun': (6, )
}
restruct.dividebyTupleCondition(
                                'weekdayRegion',
                                condition_only_sun
                                )
restruct.deleteRegion('weekdayRegion')
restruct.commitRestructedData()

data.slicebyTrainTestStructure(y= 'y_sum')

doprophet= Prophet_timeseries(dataclass= data)
doprophet.addModel('weekday,object', 'day', regressor= 'rain_amount')
doprophet.fit('weekday,object')
r= Result()
doprophet.forecast('weekday,object', r.forecast_dict)
print(r.forecast_dict)

r.mergeResult(by='concat', m_name='weekday,object')
r.calcErrRate()
r.printErrRate()
