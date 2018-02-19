import os, sys
path_name= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from _element import varr

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import copy
from datetime import datetime, timedelta
from collections import OrderedDict

def xlsx_opener(inputfilename, df_dir= varr.PJ_DIR + varr.DF_DIR, merged= True, inputsheetname= None):
    '''
    엑셀 파일을 엽니다.
    현재는 특정한 디렉토리가 inputfilename에 적혀져 있어야 열릴 수 있는 상태입니다.
    '''
    xls= pd.ExcelFile(df_dir+inputfilename)
    if not inputsheetname: inputsheetname= xls.sheet_names
    if merged:
        df_txs= pd.DataFrame()
        for sheet_name in inputsheetname:
            df= xls.parse(sheet_name)
            df_txs= pd.concat([df_txs, df])
        return df_txs
    else:
        dict_of_dfs = {}
        for sheet_name in inputsheetname:
            dict_of_dfs[sheet_name] = xls.parse(sheet_name)
        return dict_of_dfs


def save_as_xlsx(df_dir, dict_of_df, inputfilename, specialfilename=None):
    """
    여러 개의 dfsheet로 되어 있는 dictionary(또는 OrderedDict) 데이터를 엑셀에 저장합니다.
    아직 디렉토리를 설정할 수 없어 나중에 수정해야 합니다.
    """
    if specialfilename==None:
        specialfilename= df_dir + inputfilename[:-5] + '_restructured' + inputfilename[-5:]
    else:
        specialfilename= df_dir + inputfilename[:-5] + specialfilename + inputfilename[-5:]
    writer= pd.ExcelWriter(specialfilename, engine= 'xlsxwriter')
    if is_dict(dict_of_df):
        for (dfsheetname, case_df) in dict_of_df.items():
            case_df['forecast'].to_excel(writer, sheet_name= dfsheetname)
    else:
        dict_of_df.to_excel(writer, sheet_name= 'data_merged')
    writer.save()
    return None


def is_dict(dict_of_dfs):
    if isinstance(dict_of_dfs, type(OrderedDict())) or isinstance(dict_of_dfs, dict):
        return True
    else: return False

def dict_to_df(dict_of_dfs):
    df_txs= pd.DataFrame()
    if is_dict(dict_of_dfs):
        for sheetname, df in dict_of_dfs.items():
            df_txs= pd.concat([df_txs, df])
    return df_txs


def struct(df, idx_col, ft_col, val_col, y_sum= False):
    """
    건수별로 이루어져 있는 df를 날짜를 index로, 건수별 유형 코드를 feature로 하는 df로 만듭니다.
    현재는 inputfilename이 input값으로 되어 있고, 이후 df를 인풋으로 하도록 수정할 예정입니다.
    또 현재는 '발송일', '유형', '수량'이라는 feature만을 가진 것으로 짜여져 있는 점,
    날짜 형식이 YYYMMDD 형식인 경우만을 고려하는 점도 수정해야 합니다.
    """
    df= df.groupby([df[idx_col], df[ft_col]])[val_col].sum().unstack(ft_col)
    df.fillna(0, inplace= True)
    if y_sum: df['y_sum']= df.sum(axis=1)
    return df


def parseIntToDatetimeShape(df, datetime_column= 'ds', datetime_format= '%Y%m%d', unite= True):
    df.ds= df.ds.map(lambda x: pd.to_datetime(x, format= datetime_format))
    uniteDatetimeShape(df)
    return df


def uniteDatetimeShape(df):
    """
    datetime을 pd.to_datetime 코드로 처리할 때, datetime.strptime 코드로 처리할 때 각각
    Timestamp, datetime dtype로 바뀌는 문제가 나타났습니다.
    이를 해결하기 위해 datetime의 type을 일정하게 유지하도록 합니다.
    """
    df['ds']= pd.to_datetime(
        df['ds'], box=True, format= '%Y/%m/%d', exact=True
        )


def dir_list(data_path, ext):
    return [os.path.join(data_path, obj) for obj in os.listdir(data_path)\
            if os.path.splitext(obj)[-1]== ext]


def cut_col(df, column_list):
    return df[column_list]

def cut_df(txs, forecastday= varr.FORECASTDAY, last_date= None):
    if not last_date:
        last_date= txs.ds.max()
    txs_train= txs[txs.ds<= last_date- timedelta(days=forecastday)]
    txs_test= txs[txs.ds> last_date- timedelta(days=forecastday)]
    return (txs_train, txs_test)

def colname(df, dict_of_colname):
    df.rename(columns= dict_of_colname, inplace= True)
    return None


def divide_multiple_y(dict_of_df, raw_key, y_col, x_col, checkpoint= None):
    for y in y_col:
        columns= copy.deepcopy(x_col)
        columns.append(y)
        keyname= y if not checkpoint else '{}_{}'.format(y, checkpoint)
        dict_of_df[keyname]= copy.deepcopy(dict_of_df[raw_key][columns])
        colname(dict_of_df[keyname], {y: 'y'})
    del dict_of_df[raw_key]
    return None

def add_division(dict_of_df, raw_key, div_num, start_num= 0, div_name= None):
    colname= 'seasonality_{},{}'.format(div_num, start_num)
    df_raw= dict_of_df[raw_key]
    season_df= pd.DataFrame(
        np.remainder(np.arange(df_raw.shape[0])+start_num, div_num),
        columns= [colname]
        )
    if div_name!= None:
        #TODO
        pass
    dict_of_df[raw_key]= dict_of_df[raw_key].join(season_df)
    return None


def divide_by(dict_of_df, raw_key, div_feature, div_set= None):
    df_raw= dict_of_df[raw_key]
    if not div_set:
        div_set= set()
        for i in df_raw[div_feature].unique():
            div_set.add((i, ))
    for division in div_set:
        dict_of_df[division]= df_raw.loc[df_raw[div_feature].isin(division)]
    del dict_of_df[raw_key]
    return None


def train_test_sample(df, y, x_col, forecastday= varr.FORECASTDAY):
    txs_raw= copy.deepcopy(df.rename(index= str, columns={y: 'y'}))
    txs_train, txs_test= cut_df(txs_raw, forecastday= forecastday)
    txs_trainX, txs_trainY= cut_col(txs_train, x_col), cut_col(txs_train, 'y')
    txs_testX= cut_col(txs_test, x_col)
    try:
        txs_testY= cut_col(txs_test, 'y')
        result_dict= {'train': txs_train,
                        'test': txs_test,
                        'trainX': txs_trainX,
                        'trainY': txs_trainY,
                        'testX': txs_testX,
                        'testY': txs_testY
                        }
    except:
        result_dict= {'train': txs_train,
                        'test': txs_test,
                        'trainX': txs_trainX,
                        'trainY': txs_trainY,
                        'testX': txs_testX,
                        }

    return result_dict
    
# Main #########################################################################

if __name__== '__main__':
    pass
