import os
import sys
path_name = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from _element import varr
from _element import feature
from _element import case

import copy
import pandas as pd
import numpy as np


class Data(dict):
    def __init__(self, df, initcasename= 'raw'):
        self.addDF(df= df, casename= initcasename)
        self._y_col= set()
        self._x_att= set()
        return None

    def addDF(self, df, casename):
        case_by_frozenset= case.Case((casename, ))
        self[case_by_frozenset]= df.copy()
        return None

    def copyDFfrom(self, copycase, case):
        self[copycase]= copy.deepcopy(self[case])



    @property
    def cases(self):
        return list(self.keys())

    def choosenCases(self, cases):
        if type(cases) == frozenset:
            return [cases]
        elif cases is None:
            return self.cases
        else:
            return case.findCasePropertiesInData(cases, self)

    def copySpecificCase(self, cases=None, copyname= 'ComparisonCase'):
        cases= self.choosenCases(cases)
        for itercase in cases:
            copycase= case.addCaseProperty(itercase, copyname)
            self.copyDFfrom(copycase, itercase)
        #TODO: unittest

    def delCases(self, cases):
        cases= self.choosenCases(cases)
        for itercase in cases:
            del self[itercase]



    @property
    def y_col(self):
        return {itercase: set(self[itercase].columns.values).difference(self._x_att)
            for itercase in list(self.keys())}

    @property
    def x_col(self):
        return {itercase: set(self[itercase].columns.values).intersection(self._x_att)
            for itercase in list(self.keys())}

    @x_col.setter
    def x_col(self, value):
        self._x_att = value

    def columnToCheck(self, col_to_check):
        return (self.y_col if col_to_check=='y' else self.x_col)

    def addMultipleXColAttribute(self, atts):
        for att in atts:
            self.addXColAttribute(att)

    def addXColAttribute(self, att):
        self._x_att.add(att)

    def removeXColAttribute(self, att):
        if att in self._x_att:
            self._x_att.remove(att)



    def changeColumnNameforCases(self, dict_of_colname, cases= None):
        cases= self.choosenCases(cases)
        for itercase in cases:
            self.changeColumnNameforOneCase(itercase, dict_of_colname)
        self.changeXColAttributefromDict(dict_of_colname)
        return None

    def changeColumnNameforOneCase(self, inputcase, dict_of_colname):
        try:
            self[inputcase].rename(
                columns= dict_of_colname, inplace= True
                )
        except:
            raise ValueError

    def changeXColAttributefromDict(self, dict_of_colname):
        for oldatt, newatt in dict_of_colname.items():
            if oldatt in self._x_att:
                self.removeXColAttribute(oldatt)
                self.addXColAttribute(newatt)



    def restructCasebyOneFeature(self, inputcase, idx_col, ft_col, val_col, y_sum= False, x_sum= False,
                        idx_to_datetime= False, datetime_format= '%Y-%m-%d'):
        """
        건수별로 이루어져 있는 df를 날짜를 index로, 건수별 유형 코드를 feature로 하는 df로 만듭니다.
        현재는 inputfilename이 input값으로 되어 있고, 이후 df를 인풋으로 하도록 수정할 예정입니다.
        또 현재는 '발송일', '유형', '수량'이라는 feature만을 가진 것으로 짜여져 있는 점,
        날짜 형식이 YYYMMDD 형식인 경우만을 고려하는 점도 수정해야 합니다.
        """
        self[inputcase]= self.groupbyOneFeature(
            self[inputcase], idx_col, ft_col, val_col
            )
        if y_sum:
            self[inputcase]= self.addSumColumn(self[inputcase], axis= 1)
        elif x_sum:
            self[inputcase] = self.addSumColumn(self[inputcase], axis=0)
        self[inputcase]= self.resetAsSimpleTable(self[inputcase], idx_col)
        if idx_to_datetime:
            self[inputcase]= feature.parseIntToDatetimeShape(
                                                    self[inputcase],
                                                    datetime_column= idx_col,
                                                    datetime_format= datetime_format
                                                    )

    def groupbyOneFeature(self, df, idx_col, ft_col, val_col):
        df= df.groupby(
            [df[idx_col], df[ft_col]]
            )[val_col].sum().unstack(ft_col)
        df.fillna(0, inplace= True)
        return df

    def addSumColumn(self, df, axis):
        columnname= ('y_sum' if axis else 'x_sum')
        df[columnname]= df.sum(axis= axis)
        return df

    def resetAsSimpleTable(self, df, idx_col):
        df.columns.name= None
        df.index.name= idx_col
        df.reset_index(drop= False, inplace= True)
        return df



    def divideCasebyColumns(self, inputcase):
        for y in self.y_col[inputcase]:
            dividecase= case.dividedCase(inputcase, y)
            self.copyDFfrom(dividecase, inputcase)
            self.selectOneYColumnInCase(y, dividecase)

    def selectOneYColumnInCase(self, y, case):
        columns= copy.deepcopy(list(self.x_col[case]))
        columns.sort()
        columns.append(y)
        self[case]= self[case][columns]



    def divideCasebyValueCondition(self, inputcase,
    dict_of_condition, name):
        condition_added_case= case.dividedCase(inputcase, name)
        for condition_name, condition in dict_of_condition.items():
            newcase= case.dividedCase(condition_added_case, condition_name)
            self[newcase]= copy.deepcopy(
                self[inputcase][
                    self[inputcase][name].isin(condition)
                    ]
                )            

    def uniqueCondition(self, series):
        uniquevalues= list(series.unique())
        uniquecount= len(uniquevalues)
        return {'{}_in_{}'.format(str(i), str(uniquecount)):(i, )
                for i in uniquevalues}



    def divideCasebyCycle(self, inputcase, cycle, cycle_name,
    start_num= 0, divide_condition= None):
        self[inputcase]= self.addCycleSeries(
            self[inputcase], cycle, cycle_name, start_num)
        if not divide_condition:
            divide_condition= self.uniqueCondition(self[inputcase][cycle_name])
        self.divideCasebyValueCondition(
            inputcase, divide_condition, cycle_name)

    def addCycleSeries(self, df, cycle, cycle_name, start_num= 0):
        len_of_raw= df.shape[0]
        cycle_df= pd.DataFrame(np.remainder(
                        np.arange(len_of_raw)+start_num, cycle),
                    columns= [cycle_name])
        return df.join(cycle_df)



    def divideCasebyPeriod(self, inputcase, period, period_name,
    start_num= 0, divide_condition= None):
        self[inputcase]= self.addPeriodSeries(
            self[inputcase], period, period_name, start_num)
        if not divide_condition:
            divide_condition= self.uniqueCondition(self[inputcase][period_name])
        self.divideCasebyValueCondition(
            inputcase, divide_condition, period_name)

    def addPeriodSeries(self, df, period, period_name, start_num= 0):
        len_of_raw= df.shape[0]
        period_df= pd.DataFrame(
                        (np.arange(len_of_raw)+start_num)//period,
                        columns= [period_name])
        return df.join(period_df)



    # def slicebyTrainTestStructure(self, y,
    # forecastday= varr.FORECASTDAY, cases= None, cv_cases= [0,1,2,3,4]):
    #     self.x_col.append('ds')
    #     if not cases:
    #         cases= copy.deepcopy(list(self.data.keys()))
    #     last_date= varr.START_DATE
    #     # for case in cases:
    #     #      last_date= max(last_date, self.data[case].ds.max())           
    #     for case in cases:
    #         last_date= self.data[case].ds.max()
    #         self.data[case].rename(index= str, columns= {y: 'y'}, inplace= True)
    #         result_dict= {}
    #         result_dict['train'], result_dict['test']= ft_c.cut_df(
    #             self.data[case], forecastday= forecastday, last_date= last_date)
    #         result_dict['trainX']= ft_c.cut_col(result_dict['train'], self.x_col)
    #         result_dict['trainY']= ft_c.cut_col(result_dict['train'], 'y')
    #         result_dict['testX']= ft_c.cut_col(result_dict['test'], self.x_col)
    #         try:
    #             result_dict['testY']= ft_c.cut_col(result_dict['test'], 'y')
    #         except:
    #             pass
    #         self.data[case]= result_dict
    #     self.x_col.remove('ds')



    def feature_not_in_data_Error(self):
        raise ValueError

    def not_in_list_Error(self):
        raise ValueError



class Table(pd.DataFrame):
    def __init__(self, dataclass, case):
        self.dataclass= dataclass
        self.case= case
        super(__class__, self).__init__(dataclass[case])

    @property
    def y_col(self):
        return list(self.dataclass.y_col[case])

    @property
    def y_columnname(self):
        if self.isYUnique():
            return self.y_col[0]
        else:
            raise AttributeError

    @y_columnname.setter
    def y_columnname(self, val):
        self.rename(index= str, columns= {self.y_columnname: val}, inplace= True)

    def isYUnique(self):
        return (len(self.y_col) == 1)



    @property
    def x_col(self):
        return self.dataclass.x_col[case]

        

    @property
    def last_date(self):
        if self.hasDS():
            return self['ds'].max()
        else:
            raise KeyError

    def hasDS(self):
        return ('ds' in self.columns.values.tolist())




if __name__== '__main__':
    print('Done')