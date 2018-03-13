
# coding: utf-8
from Cython import *
from scipy import optimize
import numpy, pandas, matplotlib, pystan, fbprophet

import os, sys
path_name= os.getcwd()
sys.path.append(path_name)
print(path_name)

from _element import feature_control as ft_c
from _element.data_control import Data, DataRestruction, DataAddition
from _element import varr

from _element.result_control import Result

from _alg.prophet import Prophet_timeseries


INPUT_FILENAME= 'KPP일별입고(13_17)_daily_obj.xlsx'
df_raw= ft_c.xlsx_opener(INPUT_FILENAME, 'C:\\Nextop\\nextop-engine\\nextop_engine\\_element\\data\\data_in_use\\')
data= Data()
data.setRawData(df_raw)

restruct= DataRestruction(data)
restruct.selectSpecificY(['y_sum'])
df_commit= restruct.commitRestructedData()
df_temp= ft_c.xlsx_opener('temp_data_merged.xlsx', 'C:\\Nextop\\nextop-engine\\nextop_engine\\_element\\data\\temp_data\\')
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
print(doprophet._model.keys())
print(doprophet._model[frozenset({'weekday,object', 'weekday'})])
doprophet.plot(frozenset({'weekday,object', 'weekday'}))
r= Result()
doprophet.forecast('weekday,object', r.forecast_dict)
print(r.forecast_dict)

r.mergeResult(by='concat', m_name='weekday,object')
r.calcErrRate()
r.printErrRate()
