import os, sys
path_name= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from _element import varr
from _element import feature_control as ft_c
from _element import calculations as calc
from _usecase import *
from datetime import datetime, timedelta
import copy


class Cross_Validation:
    def __init__(self, dataclass):
        self._origin_instance= dataclass
        self.data= copy.deepcopy(dataclass.data)
        self.y_col= dataclass.y_col
        self.x_col= dataclass.x_col
        self._info= {}
        self._result= {}
        self._forecast= {}
        self._err_rate= tuple()


    def slice(self, y, forecastday= varr.FORECASTDAY, num_of_data= 5, delay= 70, recent= True):
        dict_df= {}
        for key, case in self.data.items():
            test_end_date= varr.LAST_DATE
            for i in range(num_of_data):
                newkey= self._origin_instance.divideKeys(key, i)
                dict_df[newkey]= case[(case['ds']<= test_end_date)]
                test_end_date= test_end_date- timedelta(days= delay)
        self.data= dict_df


    def returntoRawData(self, data):
        self._origin_instance.resetRawData(data)
        self.__init__(self._origin_instance)

    def commitRestructedData(self):
        self._origin_instance.data= self.data
        return copy.deepcopy(self.data)