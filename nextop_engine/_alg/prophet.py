import os, sys
path_name = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

import _element.feature_control as ft_c
import _element.calculations as calc
import _element.varr as varr

import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from fbprophet import Prophet
from collections import OrderedDict
from scipy.special import expit
from scipy.stats import pearsonr
import copy
import collections

# Prophet ######

class Prophet_timeseries:
    def __init__(self, cv= False):
        self._model= {}
        self.txs_traintest= None
        self.cv= cv


    def add_data(txs_traintest):
        self.txs_traintest= txs_traintest
        return None


    def validate(self):
        '''
        데이터가 Prophet Alg를 수행하기 적합한지 검사합니다.
        검사하는 항목에는 train/test가 나누어져 있는지,
        컬럼에 ds, y가 있는지, 시계열 데이터인지 등이 포함됩니다.
        '''
        if not type(self.txs_traintest)== dict:
            raise Typeerror
        if not ('ds'in self.txs_traintest.columns.values.tolist())\
        or ('y' in self.txs_traintest.columns.values.tolist()):
            raise Valueerror('ds or y is not provided.')
        #TODO: 시계열 데이터인지 validate
        print(self.txs_traintest['trainX'].columns.values.tolist())
        print(self.txs_traintest['trainY'].columns.values.tolist())
        return None


    def add_model(self, name, unit, holidaybeta = varr.HOLYDAYBETA, regressor= True, short_turm= False):
        self._model[name]= {}
        self._model[name]['seasonality']= set((7, 30.5, 365))

        if unit is 'week':
            self._model[name]['seasonality'].remove(7)
        elif unit is 'month':
            self._model[name]['seasonality'].remove(7)
            self._model[name]['seasonality'].remove(30.5)
        if short_turm:
            self._model[name]['seasonality'].remove(365)

        self._model[name]['model'] = Prophet(daily_seasonality= (1 in self._model[name]['seasonality']),
                                            weekly_seasonality=False,
                                            yearly_seasonality= (365 in self._model[name]['seasonality']),
                                            holidays=holidaybeta)

        if 30.5 in self._model[name]['seasonality']:
            self._model[name]['model'].add_seasonality(name='monthly', period=30.5, fourier_order=5)
        if 7 in self._model[name]['seasonality']:
            self._model[name]['model'].add_seasonality(name='weekly', period=7, fourier_order=5, prior_scale=0.1)

        if type(regressor)== list:
            for feature in regressor:
                if not feature== 'ds': self._model[name]['model'].add_regressor(feature)
        elif regressor:
            for feature in self.txs_traintest['trainX'].columns.values.tolist():
                if not feature == 'ds': self._model[name]['model'].add_regressor(feature)
        else:
            pass

        self._model[name]['modelname']= name
        self._model[name]['unit']= unit
        self._model[name]['holidaybeta']= holidaybeta
        self._model[name]['regressor']= regressor


    def add_seasonality(self, m_name, period, s_name, f_order= 3, scale= 0.05):
        if type(period)== (float or int):
            self._model[m_name]['model'].add_seasonality(name= name, period= period, fourier_order= f_order, prior_scale= scale)
            self._model[m_name]['seasonality'].add(period)
        elif isinstance(period, collections.Iterable):
            for i in period:
                i_name= '{}_{}'.format(name, str(i))
                self._model[m_name]['model'].add_seasonality(name= I_name, period= i, fourier_order= f_order, prior_scale= scale)
            self._model[m_name]['seasonality'].update(period)
        else:
            raise Typeerror('incorrect period varr')
        return None


     # add_regressor: Prophet 내부 함수 add_regressor(feature)로 추가 가능


    def add_regressor(self):
        # TODO: 작성
        return None


    def add_event(self):
        # TODO: 작성
        return None


    def remove_event(self):
        # TODO: 작성
        return None


    def fit(self, m_name, txs_traintest= None):
        if txs_traintest:
            self.txs_traintest= txs_traintest
        elif self.txs_traintest is None:
            raise Keyerror('no data given')
        else:
            pass

        if not self.cv:
            self._model[m_name]['model'].fit(self.txs_traintest['train'])
        
            if 'testX' in self.txs_traintest.keys():
                self._model[m_name]['futuredate']= pd.concat([self.txs_traintest['trainX'], self.txs_traintest['testX']],
                                                            axis= 0)
                self._model[m_name]['forecastProphetTable']= self._model[m_name]['model'].predict(self._model[m_name]['futuredate'])
            else:
                self._model[m_name]['futuredate']= Valueerror('error in table func')
                self._model[m_name]['forecastProphetTable']= Valueerror('error in table func')
        elif self.cv:
            for i, case_dict in self.txs_traintest.items():
                m_name_withi= '{}_{}'.format(m_name, str(i))
                self._model[m_name_withi]= copy.deepcopy(self._model[m_name])
                self._model[m_name_withi]['model'].fit(case_dict['train'])
            
                if 'testX' in case_dict.keys():
                    self._model[m_name_withi]['futuredate']= pd.concat([case_dict['trainX'], case_dict['testX']],
                                                                axis= 0)
                    self._model[m_name_withi]['forecastProphetTable']= self._model[m_name_withi]['model'].predict(self._model[m_name_withi]['futuredate'])
                else:
                    self._model[m_name_withi]['futuredate']= Valueerror('error in table func')
                    self._model[m_name_withi]['forecastProphetTable']= Valueerror('error in table func')
        
        return None


    def forecast(self, m_name, forecast_dict):
        if not self.cv:
            result_forecast = self._model[m_name]['forecastProphetTable'][['ds', 'yhat']]
            result_forecast['ds']= pd.to_datetime(
                result_forecast['ds'], box=True, format= '%Y/%m/%d', exact=True
                )
            self.txs_traintest['test']['ds']= pd.to_datetime(
                self.txs_traintest['test']['ds'], box=True, format= '%Y/%m/%d', exact=True
                )
            forecast_dict.update({
                m_name:
                    {'forecast':
                    pd.merge(self.txs_traintest['test'], result_forecast, how='left', on='ds')}
                })
        elif self.cv:
            for i, case_dict in self.txs_traintest.items():
                m_name_withi= '{}_{}'.format(m_name, str(i))
                result_forecast = self._model[m_name_withi]['forecastProphetTable'][['ds', 'yhat']]
                result_forecast['ds']= pd.to_datetime(
                    result_forecast['ds'], box=True, format= '%Y/%m/%d', exact=True
                    )
                self.txs_traintest[i]['test']['ds']= pd.to_datetime(
                    self.txs_traintest[i]['test']['ds'], box=True, format= '%Y/%m/%d', exact=True
                    )
                forecast_dict.update({
                    m_name_withi:
                        {'forecast':
                        pd.merge(self.txs_traintest[i]['test'], result_forecast, how='left', on='ds')}
                    })
        return None


    def save_result(self, m_name, category, element, forecast_dict):
        for i, case_dict in self._model.items():
            if m_name in i:
                forecast_dict.update({
                    i:
                    {category: element}
                    })


    def extract(self, m_name, feature_list):
         abs_list= self._model[m_name]['forecastProphetTable'][feature_list].sum(axis= 1).abs()
         return self._model[m_name]['forecastProphetTable'][abs_list>0][feature_list]




