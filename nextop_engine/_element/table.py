import os
import sys
path_name = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from _element import predictionmodel

import pandas as pd

class Table(pd.DataFrame):
    def setDFCase(self, dataclass, case, forecastday= varr.FORECASTDAY):
        self.dataclass= dataclass
        self.case= case
        self.forecastday= forecastday
        self.model= predictionmodel.PredictionCases()

    @property
    def y_col(self):
        return list(
                set(self.columns.values).difference(self.dataclass._x_att)
                )

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
        return list(
                set(self.columns.values).intersection(self.dataclass._x_att)
                )

        

    @property
    def last_date(self):
        if self.hasDS():
            return self['ds'].max()
        else:
            raise KeyError

    def hasDS(self):
        return ('ds' in self.columns.values.tolist())



    @property
    def XX(self):
        return self[self.x_col]

    @property
    def YY(self):
        return self[self.y_col]

    @property
    def train(self):
        return self[self['ds'] <= self.last_date - timedelta(
                    days= self.forecastday
                    )]

    @property
    def test(self):
        return self[self['ds'] > self.last_date - timedelta(
                    days= self.forecastday
                    )]

    @property
    def trainX(self):
        return self.train[self.x_col]

    @property
    def trainY(self):
        return self.train[self.y_col]

    @property
    def testX(self):
        return self.test[self.x_col]

    @property
    def testY(self):
        return self.test[self.y_col]