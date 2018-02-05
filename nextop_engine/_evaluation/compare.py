import os, sys
path_name= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from _element import varr
from _element import feature_control as ft_c
from _element import calculations as calc
from _usecase import *
from datetime import datetime, timedelta

def AlgorithmCompare(testY, algorithm):
    global mockForecastDictionary
    nameOfBestAlgorithm = 'LSTM'
    minData = calc.rms_error(testY, mockForecastDictionary[nameOfBestAlgorithm])
    rms = 0
    for algorithm in mockForecastDictionary.keys():
        rms = calc.rms_error(testY, mockForecastDictionary[algorithm])
        if rms < minData:
            nameOfBestAlgorithm = algorithm
    print('testY is: ', testY)
    print('\n')
    print('LSTM forecast :', mockForecastDictionary['LSTM'], '\n@@@@@LSTM calculation.rms_error: ',
          calc.rms_error(testY, mockForecastDictionary['LSTM']))
    print('Bayseian forecast :', mockForecastDictionary['Bayseian'], '\n@@@@@Bayseian calculation.rms_error: ',
          calc.rms_error(testY, mockForecastDictionary['Bayseian']))
    print('\n')
    print(nameOfBestAlgorithm, 'WON!!!!!!')
    return nameOfBestAlgorithm

def print_err_rate(forecast_dict, m_name= ''):
    for i, case_dict in forecast_dict.items():
        if m_name in i:
            print('RMSE with segment {}: {:0.4f}'.format(i, case_dict['RMSE']))
            print('MAPE with segment {}: {:0.4f}'.format(i, case_dict['MAPE']))
            print('MAPE_with_std with segment {}: {:0.4f}'.format(i, case_dict['MAPE_with_std']))
            print('MAPE_div_std with segment {}: {:0.4f}'.format(i, case_dict['MAPE_div_std']))
            print('sMAPE with segment {}: {:0.4f}'.format(i, case_dict['sMAPE']))
            print('\n')
    return None

def err_rate(forecast_dict):
    for i, case_dict in forecast_dict.items():
        case_dict['RMSE']= calc.rms_error(case_dict['forecast']['y'], case_dict['forecast']['yhat'])
        case_dict['MAPE'] = calc.map_error(case_dict['forecast']['y'], case_dict['forecast']['yhat'])
        case_dict['MAPE_with_std'] = calc.map_error_with_std(case_dict['forecast']['y'], case_dict['forecast']['yhat'])
        case_dict['MAPE_div_std'] = calc.map_error_div_std(case_dict['forecast']['y'], case_dict['forecast']['yhat'])
        case_dict['sMAPE'] = calc.smap_error(case_dict['forecast']['y'], case_dict['forecast']['yhat'])

def plot_result():
    # TODO: plot_result 구현
    return None

class Cross_Validation:
    def __init__(self, df):
        self._data= df
        self._info= {}
        self._result= {}
        self._forecast= {}
        self._err_rate= tuple()


    def slice(self, y, x_col, forecastday= varr.FORECASTDAY, num_of_data= 5, delay= 70, recent= True):
        test_end_date= varr.LAST_DATE
        cv_dict= {}
        for i in range(num_of_data):
            cv_dict[i]= ft_c.train_test_sample(self._data[(self._data['ds']<= test_end_date)],
                                               y,
                                               x_col,
                                               forecastday= forecastday
                                               )
            test_end_date= test_end_date- timedelta(days= delay)
        self._data= cv_dict

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
