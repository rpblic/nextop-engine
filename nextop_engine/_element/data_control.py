import os, sys
path_name= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from _element import varr
from _element import feature_control as ft_c

import copy
import pandas as pd
import numpy as np


class Data:
    def __init__(self):
        self.data= {}
        self.grabdata= None
        self.grabcase= None
        self.y_col= []
        self.x_col= []


    # def setRawData(self, df, dataname= 'raw', rawdata_setting= True):
    #     if rawdata_setting:
    #         self.data= {}
    #     self.addData(df= df, dataname= dataname)
    #     self.setRawYColumn(case= frozenset([dataname, ]))
    #     self.setGrabData(case= frozenset([dataname, ]))
    #     return None


    # def addData(self, df, dataname,
    #             printdata= True):
    #     self.data[frozenset([dataname, ])]= df.copy()
    #     if printdata:
    #         self.showData()
    #     return None


    # def setRawYColumn(self, case):
    #     try:
    #         self.y_col= self.data[case].columns.values.tolist()
    #         self.y_col.remove('ds')
    #     except:
    #         return None


    # def setGrabData(self, case):
    #     self.grabdata= self.data[case]
    #     self.grabcase= case


    def resetRawDataDict(self, data):
        self.data= {}
        self.data= data


    # def showData(self):
    #     for key in self.data.keys():
    #         try:
    #             print(self.data[key].head())
    #             print(self.data[key].info())
    #         except AttributeError:
    #             pass


    # def divideKeys(self, key, addon, raw= 'raw'):
    #     resultkey= key.copy().union(frozenset((addon, )))
    #     if raw in resultkey:
    #         resultkey= resultkey- frozenset((raw, ))
    #     return resultkey


    def slicebyTrainTestStructure(self, y,
                                forecastday= varr.FORECASTDAY, cases= None, cv_cases= [0,1,2,3,4]):
        self.x_col.append('ds')
        if not cases:
            cases= copy.deepcopy(list(self.data.keys()))
        last_date= varr.START_DATE
        # for case in cases:
        #      last_date= max(last_date, self.data[case].ds.max())           
        for case in cases:
            last_date= self.data[case].ds.max()
            self.data[case].rename(index= str, columns= {y: 'y'}, inplace= True)
            result_dict= {}
            result_dict['train'], result_dict['test']= ft_c.cut_df(
                self.data[case], forecastday= forecastday, last_date= last_date)
            result_dict['trainX']= ft_c.cut_col(result_dict['train'], self.x_col)
            result_dict['trainY']= ft_c.cut_col(result_dict['train'], 'y')
            result_dict['testX']= ft_c.cut_col(result_dict['test'], self.x_col)
            try:
                result_dict['testY']= ft_c.cut_col(result_dict['test'], 'y')
            except:
                pass
            self.data[case]= result_dict
        self.x_col.remove('ds')


class DataRestruction:
    def __init__(self, dataclass):
        self._origin_instance= dataclass
        self.data= copy.deepcopy(dataclass.data)
        self.y_col= dataclass.y_col
        self.x_col= dataclass.x_col
        self.grabdata= dataclass.grabdata
        self.grabcase= dataclass.grabcase


    # def changeColumnName(self, dict_of_colname):
    #     for i, df in self.data.items():
    #         df.rename(columns= dict_of_colname, inplace= True)
    #     return None


    # def groupbyObject(self, idx_col, ft_col, val_col, idx_name= 'ds', y_sum= False,
    #                     idx_to_datetime= False, datetime_format= '%Y%m%d'):
    #     """
    #     건수별로 이루어져 있는 df를 날짜를 index로, 건수별 유형 코드를 feature로 하는 df로 만듭니다.
    #     현재는 inputfilename이 input값으로 되어 있고, 이후 df를 인풋으로 하도록 수정할 예정입니다.
    #     또 현재는 '발송일', '유형', '수량'이라는 feature만을 가진 것으로 짜여져 있는 점,
    #     날짜 형식이 YYYMMDD 형식인 경우만을 고려하는 점도 수정해야 합니다.
    #     """
    #     for case in self.data.keys():
    #         self.data[case]= self.data[case].groupby(
    #             [self.data[case][idx_col], self.data[case][ft_col]]
    #             )[val_col].sum().unstack(ft_col)
    #         self.data[case].fillna(0, inplace= True)
    #         if y_sum:
    #             self.data[case]['y_sum']= self.data[case].sum(axis=1)
    #         self.data[case].columns.name= None
    #         self.data[case].index.name= idx_name
    #         self.data[case].reset_index(drop= False, inplace= True)
    #         if idx_to_datetime:
    #             self.data[case]= ft_c.parseIntToDatetimeShape(
    #                                                             self.data[case],
    #                                                             datetime_column= idx_name,
    #                                                             datetime_format= datetime_format
    #                                                             )


    # def setComparisonCase(self, case):
    #     comparisonkey= self.divideKeys(case, 'ComparisonCase')
    #     self.data[comparisonkey]= copy.deepcopy(self.data[case])


    def selectSpecificY(self, y_col, cases= None):
        if not cases:
            cases= copy.deepcopy(list(self.data.keys()))

        y_col.append('ds')
        for case in cases:
            self.data[case]= self.data[case][y_col]
        self.y_col= y_col
        self.y_col.remove('ds')


    def divideKeys(self, key, addon, raw= 'raw'):
        resultkey= key.copy().union(frozenset((addon, )))
        if raw in resultkey:
            resultkey= resultkey- frozenset((raw, ))
        return resultkey


    # def divideCase(self, y_col, cases= None):
    #     if not cases:
    #         cases= copy.deepcopy(list(self.data.keys()))
    #     for case in cases:
    #         for y in y_col:
    #             newcase= self.divideKeys(case, y)
    #             self.data[newcase]= copy.deepcopy(self.data[case])
    #             for y_to_delete in y_col:
    #                 if y_to_delete!= y:
    #                     self.data[newcase].drop(y_to_delete, inplace= True)


    # def deleteCase(self, cases_to_del):
    #     if ((type(cases_to_del) is list) or
    #         (type(cases_to_del) is set) or
    #         (type(cases_to_del) is tuple)):
    #         for case in cases_to_del:
    #             self.data.pop(case, None)
    #     elif type(cases_to_del)== str:
    #         for case in list(self.data.keys()):
    #             if cases_to_del in case:
    #                 self.data.pop(case, None)
    #     else:
    #         raise TypeError


    # def divideRegion(self, region_num, region_name, start_num= 0,
    #                 region_condition= None, deleteraw= True, cases= None):
    #     if not cases:
    #         cases= copy.deepcopy(list(self.data.keys()))
    #     self.addRegion(region_num, region_name, start_num, cases)
    #     if not region_condition:
    #         region_condition= self.defaultRegionCondtion(region_num, region_name)
    #     self.dividebyTupleCondition(
    #         region_name= region_name,
    #         region_condition= region_condition,
    #         deleteraw= deleteraw,
    #         cases= cases)
    #     self.deleteRegion(region_name)


    # def addRegion(self, region_num, region_name, start_num= 0,
    #                 cases= None):
    #     if not cases:
    #         cases= copy.deepcopy(list(self.data.keys()))
    #     for case in cases:
    #         region_df= pd.DataFrame(
    #                             np.remainder(
    #                                 np.arange(self.data[case].shape[0])
    #                                 +start_num, region_num
    #                                 ),
    #                             columns= [region_name]
    #                             )
    #         self.data[case]= self.data[case].join(region_df)

    # def deleteRegion(self, region_name):
    #     cases= copy.deepcopy(list(self.data.keys()))
    #     for case in cases:
    #         try:
    #             self.data[case].drop(region_name, axis= 1, inplace= True)
    #         except KeyError:
    #             pass

    # def dividebyTupleCondition(self, region_name, region_condition,
    #                             deleteraw= True, cases= None):
    #     if not cases:
    #         cases= copy.deepcopy(list(self.data.keys()))
    #     addon_dict= {}
    #     for case in cases:
    #         for condition in region_condition.keys():
    #             newcase= self.divideKeys(case, condition)
    #             addon_dict[newcase]= copy.deepcopy(
    #                 self.data[case][
    #                     self.data[case][region_name].isin(
    #                         region_condition[condition]
    #                         )
    #                     ]
    #                 )
    #     self.data.update(addon_dict)
    #     if deleteraw:
    #         self.deleteCase(cases)

    # def defaultRegionCondtion(self, region_num, region_name):
    #     default_condition_dict= {}
    #     for i in range(region_num):
    #         key= '{}_{}'.format(region_name, str(i))
    #         condition= (i, )
    #         default_condition_dict[key]= condition
    #     return default_condition_dict


    def returntoRawData(self, data):
        self._origin_instance.resetRawData(data)
        self.__init__(self._origin_instance)

    def commitRestructedData(self):
        self._origin_instance.data= self.data
        self._origin_instance.y_col= self.y_col
        self._origin_instance.showData()
        try:
            self._origin_instance.grabdata= self._origin_instance.data[self._origin_instance.grabcase]
        except KeyError:
            print('original grabcase expired; please take another case as grabcase.')



class DataAddition:
    def __init__(self, dataclass):
        self._origin_instance= dataclass
        self.data= dataclass.data
        self.x_col= dataclass.x_col
        self.y_col= dataclass.y_col
        self.grabdata= dataclass.grabdata
        self.grabcase= dataclass.grabcase


    def addXData(self, df_addon, cases= None):
        if not cases:
            cases= copy.deepcopy(list(self.data.keys()))
        self.x_col.extend(
            df_addon.columns.values.tolist()
            )
        self.x_col.remove('ds')

        for case in cases:
            ft_c.uniteDatetimeShape(self.data[case])
            ft_c.uniteDatetimeShape(df_addon)
            self.data[case]= pd.merge(
                self.data[case], df_addon, how= 'inner', on= 'ds'
                )


    def returntoRawData(self, data):
        self._origin_instance.resetRawData(data)
        self.__init__(self._origin_instance)

    def commitAddedData(self):
        self._origin_instance.data= self.data
        self._origin_instance.x_col= self.x_col
        try:
            self._origin_instance.grabdata= self._origin_instance.data[self._origin_instance.grabcase]
        except KeyError:
            print('original grabcase expired; please take another case as grabcase.')
        self._origin_instance.showData()
