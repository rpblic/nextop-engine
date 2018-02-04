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
    def __init__(self, unit, holidaybeta = varr.HOLYDAYBETA, regressor= True):
        self.seasonality= set(1, 7, 30.5, 365)
        if unit is 'day':
            self.seasonality.remove(1)
            if (len(txs_train) < 366):
                self.seasonality.remove(365)

        elif unit is 'week':
            self.seasonality.remove(1, 7)
            if (len(txs_train) < 53):
                self.seasonality.remove(365)

        elif unit is 'month':
            self.seasonality.remove(1, 7, 30.5)
            if (len(txs_train) < 12):
                self.seasonality.remove(365)

        self._model = Prophet(daily_seasonality=self.seasonality[0],
                        weekly_seasonality=False,
                        yearly_seasonality=self.seasonality[3],
                        holidays=holidaybeta)

        if self.seasonality[2]:
            self._model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        if self.seasonality[1]:
            self._model.add_seasonality(name='weekly', period=7, fourier_order=5, prior_scale=0.1)

        if type(regressor)== list:
            for feature in regressor:
                if not feature== 'ds': self._model.add_regressor(feature)
        elif regressor:
            for feature in self.txs_traintest['trainX'].columns.values.tolist():
                if not feature == 'ds': self._model.add_regressor(feature)
        else:
            pass

        self.unit= unit
        self.holidaybeta= holidaybeta
        self.regressor= regressor
        self.txs_traintest= None


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


    def add_data(txs_traintest):
        self.txs_traintest= txs_traintest
        return None


    def add_seasonality(self, period, name, f_order= 3, scale= 0.05):
        if type(period)== (float or int):
            self._model.add_seasonality(name= name, period= period, fourier_order= f_order, prior_scale= scale)
            self.seasonality.add(period)
        elif isinstance(period, collections.Iterable):
            for i in period:
                i_name= '{}_{}'.format(name, str(i))
                self._model.add_seasonality(name= I_name, period= i, fourier_order= f_order, prior_scale= scale)
            self.seasonality.update(period)
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


    def fit(self, txs_traintest= None):
        if txs_traintest:
            self.txs_traintest= txs_traintest
        elif self.txs_traintest is None:
            raise Keyerror('no data given')
        else:
            pass

        self._model.fit(self.txs_traintest['train'])
        
        if 'testX' in self.txs_traintest.keys():
            self.futuredate= pd.concat(self.txs_traintest['trainX'],
                                        self.txs_traintest['testX'],
                                        axis= 0)
            self._forecastProphetTable= self._model.predict(self.futuredate)
        else:
            self.futuredate= Valueerror('error in table func')
            self._forecastProphetTable= Valueerror('error in table func')
        return None


    def forecast(self, forecast_dict, name):
        result_forecast = forecastProphetTable[['ds', 'yhat']]
        result_forecast['ds']= pd.to_datetime(
            result_forecast['ds'], box=True, format= '%Y/%m/%d', exact=True
            )
        self.txs_traintest['testX']['ds']= pd.to_datetime(
            self.txs_traintest['testX']['ds'], box=True, format= '%Y/%m/%d', exact=True
            )
        forecast_dict.update({
            name:
                {'forecast':
                pd.merge(self.txs_traintest['testX'], result_forecast, how='left', on='ds')}
            })
        return None


    def extract(self, feature_list):
         abs_list= self._forecastProphetTable[feature_list].sum(axis= 1).abs()
         return self._forecastProphetTable[abs_list>0][feature_list]




