import os
import sys

path_name = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)
# print(os.path.dirname(__file__))
import _element.feature_control as ft_c
import _element.calculations as calc
import _element.varr as varr

# 이미 수정한 데이터로 진행
df_dir = varr.DF_DIR
temp_data_dir = varr.TEMP_DATA_DIR
holidaybeta = varr.HOLYDAYBETA

import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from fbprophet import Prophet
from collections import OrderedDict
from scipy.special import expit
from scipy.stats import pearsonr
import copy


def Bayseian2(txs_traintest, unit, holidaybeta = varr.HOLYDAYBETA):
    global seasonality_option
    txs_train = txs_traintest['train']
    txs_test = txs_traintest['test']
    txs_trainX = txs_traintest['trainX']
    txs_trainY = txs_traintest['trainY']
    txs_testX = txs_traintest['testX']
    txs_testY = txs_traintest['testY']

    if unit is 'day':
        if (len(txs_train) < 366):
            seasonality_option = (False, True, True, False, 'd')
        else:
            seasonality_option = (False, True, True, True, 'd')

    elif unit is 'week':
        if (len(txs_train) < 53):
            seasonality_option = (False, False, True, False, 'w')
        else:
            seasonality_option = (False, False, True, True, 'w')

    elif unit is 'month':
        if (len(txs_train) < 12):
            seasonality_option = (False, False, False, False, 'm')
        else:
            seasonality_option = (False, False, False, True, 'm')

    model = Prophet(daily_seasonality=seasonality_option[0],
                    weekly_seasonality=False,
                    yearly_seasonality=seasonality_option[3],
                    holidays=holidaybeta)

    if seasonality_option[2]:
        model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    if seasonality_option[1]:
        model.add_seasonality(name='weekly', period=7, fourier_order=5, prior_scale=0.1)

    for feature in txs_trainX.columns.values.tolist():
        if not feature == 'ds': model.add_regressor(feature)

    model.fit(txs_train)
    future = pd.concat([txs_trainX, txs_testX], axis=0)

    forecastProphetTable = model.predict(future)
    return {
        'model': model,
        'future': future,
        'forecastProphetTable': forecastProphetTable
    }
    # date = [d.strftime('%Y-%m-%d') for d in forecastProphetTable['ds']]


def extract_info_from(future, forecastProphetTable, forecastDay):
    result_forecast = forecastProphetTable[['ds', 'yhat']][-forecastDay:]
    result_forecast['ds'] = result_forecast['ds'].map(lambda x: x.to_pydatetime())
    expit(result_forecast['yhat'])
    # print(result_forecast)
    # result_df= pd.concat([future[-forecastDay:], result_forecast], axis=1)
    result_df = pd.merge(future[-forecastDay:], result_forecast, how='inner', on='ds')
    # future[-forecastDay:].join(result_forecast, how='left', on= 'ds', lsuffix= '_left', rsuffix= '_right')
    if 'newyear' in forecastProphetTable.columns.values.tolist():
        event_parameter_df = forecastProphetTable[
            (forecastProphetTable['newyear'] +
             forecastProphetTable['thanksgiving'] +
             forecastProphetTable['chocostick'] +
             forecastProphetTable['christmas'] +
             forecastProphetTable['newyearbefore'] +
             forecastProphetTable['thanksgivingbefore']).abs() > 0][ \
            ['ds', 'newyear', 'thanksgiving', 'chocostick', 'christmas', 'newyearbefore', 'thanksgivingbefore']]
    else: event_parameter_df= None
    return {'result_forecast': result_forecast, 'result_df': result_df, \
            'event_parameter_df': event_parameter_df}


def find_seasonality(df, y):
    for i in range(365):
        (corr, p_val) = pearsonr(df[y].iloc[i:], df[y].shift(i).iloc[i:])
        print('case {}: p_value is {}'.format(i, p_val))
    return None


# TODO : 페이스북 라이브러리 조절 파라메터 도큐멘 공부해서 성능 높이기

# Main ########################################################################
if __name__ == '__main__':
    txs = pd.read_excel('KPP일별투입(10_17)_restructured_restructured.xlsx', header=0)
    if ft_c.is_dict(txs):
        txs = ft_c.dict_to_df(txs, varr.COLNAME_KPPDAILY)

    (model, future, forecastProphetTable) = Bayseian2(txs, varr.FORECASTDAY, 'day')
    (result_forecast, result_df, event_parameter_df) = extract_info_from(future, forecastProphetTable, varr.FORECASTDAY)

    print(result_df)
    print(forecastProphetTable.head(20))
    print(event_parameter_df)

    # model.plot(forecastProphetTable)
    # model.plot_components(forecastProphetTable)
    print(calc.rms_error(result_df['y'], result_df['yhat']))
    print(calc.map_error(result_df['y'], result_df['yhat']))

