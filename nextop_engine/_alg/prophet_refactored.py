import os, sys
path_name = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from _element import data, case, feature, result, varr
import _element.calculations as calc


import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from fbprophet import Prophet
from collections import OrderedDict
from scipy.special import expit
from scipy.stats import pearsonr
import copy
import collections
import matplotlib.pyplot as plt

# Prophet ######

class Prophet_timeseries:
    def __init__(self, dataclass= None):
        if not dataclass is None:
            self._origin_instance= dataclass
            self.txs_traintest= dataclass.data
            self.y_col= dataclass.y_col
            self.x_col= dataclass.x_col
        self._model= {}


    def addData(dataclass):
        self._origin_instance= dataclass
        self.txs_traintest= dataclass.data
        self.y_col= dataclass.y_col
        self.x_col= dataclass.x_col
        return None


    def validateData(self):
        '''
        데이터가 Prophet Alg를 수행하기 적합한지 검사합니다.
        검사하는 항목에는 train/test가 나누어져 있는지,
        컬럼에 ds, y가 있는지, 시계열 데이터인지 등이 포함됩니다.
        '''
        if not type(self.txs_traintest)== dict:
            raise Typeerror
        if not (
                ('ds'in self.txs_traintest.columns.values.tolist())
                or ('y' in self.txs_traintest.columns.values.tolist())
                ):
            raise Valueerror('ds or y is not provided.')
        #TODO: 시계열 데이터인지 validate
        print(self.txs_traintest['trainX'].columns.values.tolist())
        print(self.txs_traintest['trainY'].columns.values.tolist())
        return None


    def addModel(self, m_name, unit,
                holidaybeta = varr.HOLYDAYBETA, regressor= True,
                growth= 'linear', short_turm= False, extra_seasonality_list= []
                ):
        self._model[m_name]= {}
        self._model[m_name]['model'] = Prophet(daily_seasonality= False,
                                            weekly_seasonality= False,
                                            yearly_seasonality= False,
                                            holidays=holidaybeta,
                                            growth= growth)

        self.setSeasonality(unit, m_name, short_turm, extra_seasonality_list)
        self.setRegressor(m_name, regressor)
        self.setEvent()
        self._model[m_name]['modelname']= m_name
        self._model[m_name]['unit']= unit
        self._model[m_name]['holidaybeta']= holidaybeta
        self._model[m_name]['regressor']= regressor


    def setSeasonality(self, unit, m_name, short_turm, extra_seasonality_list):
        self.defaultSeasonalitySetting(unit, m_name, short_turm)
        for period in extra_seasonality_list:
            self.addSeasonDict(m_name, period)
        for period, seasonality_dict in self._model[m_name]['seasonality'].items():
            self.addSeasonality(
                                m_name, period,
                                s_name= seasonality_dict['name'],
                                f_order= seasonality_dict['f_order'],
                                scale= seasonality_dict['scale']
                                )
        return None


    def defaultSeasonalitySetting(self, unit, m_name, short_turm):
        self._model[m_name]['seasonality']= {
                                            7: {'name': 'weekly', 'f_order': 5, 'scale': 0.1},
                                            30.5: {'name': 'monthly', 'f_order': 3, 'scale': 0.05},
                                            365: {'name': 'yearly', 'f_order': 3, 'scale': 0.05},
                                            }
        if unit is 'day':
            pass
        elif unit is 'week':
            del self._model[m_name]['seasonality'][7]
        elif unit is 'month':
            del self._model[m_name]['seasonality'][7]
            del self._model[m_name]['seasonality'][30.5]
        if short_turm:
            del self._model[m_name]['seasonality'][365]
        return None


    def addSeasonDict(self, m_name, period, s_name= None, f_order= 3, scale= 0.05):
        if s_name is None:
            s_name= 'seasonality_{}'.format(period)
        self._model[m_name]['seasonality'][period]= {
                                                    'name': s_name,
                                                    'f_order': f_order,
                                                    'scale': scale
                                                    }


    def addSeasonality(self, m_name, period, s_name, f_order, scale):
        self._model[m_name]['model'].add_seasonality(
                                                    name= s_name,
                                                    period= period,
                                                    fourier_order= f_order,
                                                    prior_scale= scale
                                                    )
        return None


    def setRegressor(self, m_name, regressor_list):
        if type(regressor_list)== list:
            for feature in regressor_list:
                if not feature== 'ds': self.addRegressor(m_name, feature)
        elif regressor_list:
            for feature in self.x_col:
                if not feature == 'ds': self.addRegressor(m_name, feature)
        elif not regressor_list:
            pass
        return None


    def addRegressor(self, m_name, feature):
        self._model[m_name]['model'].add_regressor(feature)
        return None


    def setEvent(self):
        # TODO: 작성
        return None


    def remove_event(self):
        # TODO: 작성
        return None


    def fit(self, m_name, log_fit= False):
        if self.txs_traintest is None:
            raise Keyerror('no data given')

        for key, case_dict in self.txs_traintest.items():
            m_name_withi= self._origin_instance.divideKeys(key, m_name)
            if log_fit:
                case_dict['train']['y']= case_dict['train']['y'].replace(to_replace= 0, value= 1)
                case_dict['train']['y']= np.log(case_dict['train']['y'])
            self._model[m_name_withi]= copy.deepcopy(self._model[m_name])
            self._model[m_name_withi]['model'].fit(case_dict['train'])
        
            if any(case_dict['testX']):
                self._model[m_name_withi]['futuredate']= pd.concat([case_dict['trainX'], case_dict['testX']],
                                                            axis= 0)
                if log_fit:
                    self._model[m_name_withi]['futuredate']['cap']= 13
                self._model[m_name_withi]['forecastProphetTable']= self._model[m_name_withi]['model'].predict(self._model[m_name_withi]['futuredate'])
                self._model[m_name_withi]['forecastProphetTable']['yhat']= self._model[m_name_withi]['forecastProphetTable']['yhat'].apply(lambda x: max(x, 0))
            elif not any(case_dict['testX']):
                raise Valueerror('error in table func')
        return None


    def forecast(self, m_name, forecast_dict):
        for case, case_dict in self.txs_traintest.items():
            m_name_withi= self._origin_instance.divideKeys(case, m_name)
            result_forecast = self._model[m_name_withi]['forecastProphetTable'][['ds', 'yhat']]
            ft_c.uniteDatetimeShape(result_forecast)
            ft_c.uniteDatetimeShape(self.txs_traintest[case]['test'])
            forecast_dict.update({
                m_name_withi:
                    {'forecast':
                    pd.merge(
                            self.txs_traintest[case]['test'],
                            result_forecast,
                            how='left', on='ds'
                            )
                    }
                })
        return None


    def save_result(self, m_name, category, element, forecast_dict):
        for case, model in self._model.items():
            if m_name in case:
                forecast_dict.update({
                    case:
                    {category: element}
                    })


    def extract(self, m_name, feature_list):
         abs_list= self._model[m_name]['forecastProphetTable'][feature_list].sum(axis= 1).abs()
         return self._model[m_name]['forecastProphetTable'][abs_list>0][feature_list]


    def plot(self, m_name):
        self._model[m_name]['model'].plot(self._model[m_name]['forecastProphetTable'])
        self._model[m_name]['model'].plot_components(self._model[m_name]['forecastProphetTable'])
        plt.show()




