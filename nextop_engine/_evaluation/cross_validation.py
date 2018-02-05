import os, sys
path_name= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from _element import varr
from _element import feature_control as ft_c
from _element import calculations as calc
from _usecase import *
from datetime import datetime, timedelta


class Cross_Validation:
    def __init__(self, df):
        self._data= df
        self._info= {}
        self._result= {}
        self._forecast= {}
        self._err_rate= tuple()


    def slice(self, y, x_col, forecastday= varr.FORECASTDAY, num_of_data= 5, delay= 70, recent= True):
        dict_df= {}
        for comp_num, comp in self._data.items():
            test_end_date= varr.LAST_DATE
            for i in range(num_of_data):
                comp_num_i= '{}_{}'.format(comp_num, i)
                dict_df[comp_num_i]= ft_c.train_test_sample(comp[(comp['ds']<= test_end_date)],
                                                                       y,
                                                                       x_col,
                                                                       forecastday= forecastday
                                                                       )
                test_end_date= test_end_date- timedelta(days= delay)
        self._data= dict_df


    def func_run(self, func, extract_func, **kwargs):
        dict_option= kwargs
        if 'forecastday' in dict_option.keys():
            forecastday= dict_option['forecastday']
        else:
            forecastday= varr.FORECASTDAY

        alg_result_dict= {}
        alg_info_dict= {}
        if self._data:
            for i, df_cv in self._data.items():
                alg_result_dict[i]= func(df_cv, **dict_option)
                alg_info_dict[i]= extract_func(
                    alg_result_dict[i]['future'],
                    alg_result_dict[i]['forecastProphetTable'],
                    forecastday
                )
        self._info= alg_info_dict
        self._result= alg_result_dict
