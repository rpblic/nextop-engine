import os, sys
path_name= 'C:\\Studying\\Project_Nextop\\nextop-engine\\nextop_engine'
sys.path.append(path_name)
print(path_name)

from _element import feature_control as ft_c
from _element.data_control import Data, DataRestruction, DataAddition
from _element import varr


INPUT_FILENAME= 'KPP일별입고(13_17)_daily_obj.xlsx'
data= Data()
data.setRawData(
    ft_c.xlsx_opener(INPUT_FILENAME, path_name+ varr.DF_DIR)
    )

restruct= DataRestruction(data)
restruct.selectSpecificY(['y_sum'])
df_commit= restruct.commitRestructedData()
df_temp= ft_c.xlsx_opener('temp_data_merged.xlsx', path_name+ varr.TEMP_DATA_DIR)
addition= DataAddition(data)
addition.addXData(df_temp)
df_commit= addition.commitAddedData()
