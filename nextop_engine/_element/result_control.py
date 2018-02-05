import os, sys
path_name = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from collections import OrderedDict
from datetime import datetime, timedelta
import _element.feature_control as ft_c
from _element import calculations as calc

import pandas as pd
import numpy as np
import copy

class Result:
    def __init__(self):
        self.forecast_dict= OrderedDict()


    def print_err_rate(self, m_name= str()):
        for i, case_dict in self.forecast_dict.items():
            if m_name in i:
                print('RMSE with segment {}: {:0.4f}'.format(i, case_dict['RMSE']))
                print('MAPE with segment {}: {:0.4f}'.format(i, case_dict['MAPE']))
                print('MAPE_with_std with segment {}: {:0.4f}'.format(i, case_dict['MAPE_with_std']))
                print('MAPE_div_std with segment {}: {:0.4f}'.format(i, case_dict['MAPE_div_std']))
                print('sMAPE with segment {}: {:0.4f}'.format(i, case_dict['sMAPE']))
                print('\n')
        return None


    def err_rate(self, m_name= str()):
        for i, case_dict in self.forecast_dict.items():
            if m_name in i:
                case_dict['RMSE']= calc.rms_error(case_dict['forecast']['y'], case_dict['forecast']['yhat'])
                case_dict['MAPE'] = calc.map_error(case_dict['forecast']['y'], case_dict['forecast']['yhat'])
                case_dict['MAPE_with_std'] = calc.map_error_with_std(case_dict['forecast']['y'], case_dict['forecast']['yhat'])
                case_dict['MAPE_div_std'] = calc.map_error_div_std(case_dict['forecast']['y'], case_dict['forecast']['yhat'])
                case_dict['sMAPE'] = calc.smap_error(case_dict['forecast']['y'], case_dict['forecast']['yhat'])


    def plot_result(self):
        # TODO: plot_result 구현
        return None


    def merge_result(self, m_name= str(), m_title= str(), delete_case= True):
        if type(m_name)== str:
            mergelist= [elmt for m_name_add, elmt in self.forecast_dict.items()
                        if (m_name in m_name_add)]
            caselist= [m_name_add for m_name_add, elmt in self.forecast_dict.items()
                        if (m_name in m_name_add)]
            merge_dict= {}
            category_list= list(mergelist[0].keys())
            for category in category_list:
                if type(mergelist[0][category])== (pd.DataFrame):
                    merge_dict[category]= pd.DataFrame()
                    for elmt in mergelist:
                        merge_dict[category]= pd.concat(
                            [merge_dict[category], elmt[category]], axis= 0
                            )
                    merge_dict[category].sort_values(
                        by= ['ds'], axis= 0, inplace= True
                        )
                else:
                    print(category, mergelist[0][category], type(mergelist[0][category]))
            self.forecast_dict['{}_{}_merged'.format(m_title, m_name)]= merge_dict
            if delete_case:
                for case in caselist:
                    del self.forecast_dict[case]

        elif type(m_name)== list:
            m_list= copy.deepcopy(m_name)
            while m_list:
                m_name= m_list.pop(0)
                mergelist= [elmt for m_name_add, elmt in self.forecast_dict.items()
                            if (m_name in m_name_add)]
                caselist= [m_name_add for m_name_add, elmt in self.forecast_dict.items()
                            if (m_name in m_name_add)]
                merge_dict= {}
                category_list= list(mergelist[0].keys())
                for category in category_list:
                    if type(mergelist[0][category])== (pd.DataFrame):
                        merge_dict[category]= pd.DataFrame()
                        for elmt in mergelist:
                            merge_dict[category]= pd.concat(
                                [merge_dict[category], elmt[category]], axis= 0
                                )
                        merge_dict[category].sort_values(
                            by= ['ds'], axis= 0, inplace= True
                            )
                    else:
                        print(category, mergelist[0][category], type(mergelist[0][category]))
                self.forecast_dict['{}_{}_merged'.format(m_title, m_name)]= merge_dict
                if delete_case:
                    for case in caselist:
                        del self.forecast_dict[case]
        return None


    def avg_result(self, m_name= str(), delete_case= True):
        if type(m_name)== str:
            mergelist= [elmt for m_name_add, elmt in self.forecast_dict.items()
                        if (m_name in m_name_add)]
            caselist= [m_name_add for m_name_add, elmt in self.forecast_dict.items()
                        if (m_name in m_name_add)]
            merge_dict= {}
            category_list= list(mergelist[0].keys())
            for category in category_list:
                if type(mergelist[0][category])== type(np.float64())\
                    or type(mergelist[0][category])== int\
                    or type(mergelist[0][category])== float:
                    merge_dict[category]= list()
                    for elmt in mergelist:
                        merge_dict[category].append(float(elmt[category]))
                    merge_dict[category]= np.mean(merge_dict[category])
                elif type(mergelist[0][category])== (pd.DataFrame):
                    merge_dict[category]= list()
                    for elmt in mergelist:
                        merge_dict[category].append(elmt[category])
                else:
                    print(category, mergelist[0][category], type(mergelist[0][category]))
            self.forecast_dict['{}_result'.format(m_name)]= merge_dict
            if delete_case:
                for case in caselist:
                    del self.forecast_dict[case]

        elif type(m_name)== list:
            m_list= copy.deepcopy(m_name)
            while m_list:
                m_name= m_list.pop(0)
                mergelist= [elmt for m_name_add, elmt in self.forecast_dict.items()
                            if (m_name in m_name_add)]
                caselist= [m_name_add for m_name_add, elmt in self.forecast_dict.items()
                            if (m_name in m_name_add)]
                merge_dict= {}
                category_list= list(mergelist[0].keys())
                for category in category_list:
                    if (type(mergelist[0][category])== type(np.float64())
                        or type(mergelist[0][category])== int
                        or type(mergelist[0][category])== float):
                        merge_dict[category]= list()
                        for elmt in mergelist:
                            merge_dict[category].append(float(elmt[category]))
                        merge_dict[category]= np.mean(merge_dict[category])
                    elif type(mergelist[0][category])== (pd.DataFrame):
                        merge_dict[category]= list()
                        for elmt in mergelist:
                            merge_dict[category].append(elmt[category])
                    else:
                        print(category, mergelist[0][category], type(mergelist[0][category]))
                self.forecast_dict['{}_result'.format(m_name)]= merge_dict
                if delete_case:
                    for case in caselist:
                        del self.forecast_dict[case]

        return None
