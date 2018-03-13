import os, sys
path_name = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from collections import OrderedDict
from datetime import datetime, timedelta
import _element.feature_control as ft_c
from _element import calculations as calc

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy

class Result:
    def __init__(self):
        self.forecast_dict= OrderedDict()


    def isIncluded(self, m_name, case_frozenset):
        if m_name is None:
            m_name= frozenset()
        return (not bool(m_name.difference(case_frozenset)))


    def printErrRate(self, m_name= None):
        for key_frozenset, case_dict in self.forecast_dict.items():
            if self.isIncluded(m_name, key_frozenset):
                print('RMSE with segment {}: {:0.4f}'.format(','.join(list(map(str, key_frozenset))), case_dict['RMSE']))
                print('MAPE with segment {}: {:0.4f}'.format(','.join(list(map(str, key_frozenset))), case_dict['MAPE']))
                print('MAPE_with_std with segment {}: {:0.4f}'.format(','.join(list(map(str, key_frozenset))), case_dict['MAPE_with_std']))
                print('MAPE_div_std with segment {}: {:0.4f}'.format(','.join(list(map(str, key_frozenset))), case_dict['MAPE_div_std']))
                print('sMAPE with segment {}: {:0.4f}'.format(','.join(list(map(str, key_frozenset))), case_dict['sMAPE']))
                print('\n')
        return None


    def calcErrRate(self, m_name= None):
        for key_frozenset, case_dict in self.forecast_dict.items():
            if self.isIncluded(m_name, key_frozenset):
                case_dict['RMSE']= calc.rms_error(case_dict['forecast']['y'], case_dict['forecast']['yhat'])
                case_dict['MAPE'] = calc.map_error(case_dict['forecast']['y'], case_dict['forecast']['yhat'])
                case_dict['MAPE_with_std'] = calc.map_error_with_std(case_dict['forecast']['y'], case_dict['forecast']['yhat'])
                case_dict['MAPE_div_std'] = calc.map_error_div_std(case_dict['forecast']['y'], case_dict['forecast']['yhat'])
                case_dict['sMAPE'] = calc.smap_error(case_dict['forecast']['y'], case_dict['forecast']['yhat'])


    def plotResult(self, m_name):
        for key_frozenset, case_dict in self.forecast_dict.items():
            if self.isIncluded(m_name, key_frozenset):
                case_dict['forecast']['y'].plot()
                case_dict['forecast']['yhat'].plot()
                plt.show()
        return None


    def mergeResult(self, by, m_name= None, delete_case= True):
        m_frozenset= self.setDefaultModelKeys(m_name= m_name)
        case_dict= self.setDefaultCaseDict(m_frozenset= m_frozenset)
        if by== 'concat':
            merge_dict= self.setConcatDict(case_dict)
            self.forecast_dict[m_frozenset]= merge_dict
        elif by== 'avg':
            merge_dict= self.setAvgDict(case_dict)
            m_frozenset= m_frozenset.union(frozenset(['result',]))
            self.forecast_dict[m_frozenset]= merge_dict
        if delete_case:
            for case in list(case_dict.keys()):
                del self.forecast_dict[case]
        return None


    def setDefaultModelKeys(self, m_name):
        if not m_name:
            m_frozenset== frozenset()
        elif type(m_name)== str:
            m_frozenset= frozenset([m_name, ])
        elif type(m_name)== (list or tuple):
            m_frozenset= frozenset(m_name)
        elif type(m_name)== type(frozenset()):
            m_frozenset= m_name
        return m_frozenset

    def setDefaultCaseDict(self, m_frozenset):
        return {case: case_dict for case, case_dict in self.forecast_dict.items()
                    if self.isIncluded(m_frozenset, case)}

    def setConcatDict(self, case_dict):
        merge_dict= {}
        for case, case_elmt in case_dict.items():
            for category, category_elmt in case_elmt.items():
                try:
                    if type(category_elmt)== (pd.DataFrame):
                        merge_dict[category]= pd.concat(
                                                        [merge_dict[category], category_elmt], axis= 0
                                                        )
                        merge_dict[category].sort_values(
                                                        by= ['ds'], axis= 0, inplace= True
                                                        )
                    else:
                        print(category, category_elmt, type(category_elmt))
                        raise TypeError
                except KeyError:
                    merge_dict[category]= category_elmt
        return merge_dict

    def setAvgDict(self, case_dict):
        merge_dict= {}
        for case, case_elmt in case_dict.items():
            for category, category_elmt in case_elmt.items():
                try:
                    if (type(category_elmt)== type(np.float64())
                        or type(category_elmt)== int
                        or type(category_elmt)== float):
                        merge_dict[category].append(float(category_elmt))
                    elif type(category_elmt)== (pd.DataFrame):
                        merge_dict[category].append(category_elmt)
                    else:
                        print(category, category_elmt, type(category_elmt))
                        raise TypeError
                except KeyError:
                    merge_dict[category]= list()
                    merge_dict[category].append(category_elmt)
        return merge_dict