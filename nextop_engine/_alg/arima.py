import os, sys
path_name= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from _element import varr

import pandas as pd
from pandas.plotting import autocorrelation_plot, lag_plot
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from collections import OrderedDict

class Arima_timeseries:
    def __init__(self):
        self._model= {}
        self.txs_traintest= None
        

    def plot(self, x_date_series, y_val_series):
        fig= plt.figure(figsize= (10, 6), dpi= 120)
        plt.plot_date(x_date_series, y_val_series, ms= 2)
        plt.show()


    def corr_check(self, series, width= 365):
        corr_dict= {}
        for i in range(width):
            corr_dict[i]= series.autocorr(lag= i)
        ordered_corr_dict= OrderedDict(sorted(corr_dict.items(),
                                                key= (lambda x: x[1]), reverse= True))
        for i, corr in ordered_corr_dict.items():
            print('lag {}: corr {}'.format(i, corr))
        autocorrelation_plot(series)
        plt.show()
            # print('case {}: p_value is {}'.format(i, p_val))
        return None


    def acf_plot(self, series):
        fig= plt.figure(figsize= (10, 11))
        ax1= fig.add_subplot(2, 1, 1)
        ax2= fig.add_subplot(2, 1, 2)
        plot_acf(series[-1095:], ax= ax1)
        plot_pacf(series[-1095:], ax= ax2)
        plt.show()


    def diff(self, series, periods, m_name):
        self._model[m_name]= {
                                'prior_series': series,
                                'periods': periods
                                }
        diffed_series= series.diff(periods= periods).iloc[periods:]
        diffed_series= pd.concat([
                                pd.Series(0, index= np.arange(periods)),
                                diffed_series
                                ])
        return diffed_series

    def undiff(self, m_list, diffed_series):
        for m_name in m_list:
            periods= self._model[m_name]['periods']
            prior_series= self._model[m_name]['prior_series']
            diffed_series+= prior_series.shift(periods)
            diffed_series[:periods]= prior_series[:periods].reset_index(drop= True)
        return diffed_series