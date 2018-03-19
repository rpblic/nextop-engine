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




def parseIntToDatetimeShape(df, datetime_column= 'ds', datetime_format= '%Y-%m-%d'):
    df[datetime_column]= df[datetime_column].map(lambda x: pd.to_datetime(x, format= datetime_format))
    uniteDatetimeShape(df, datetime_format)
    return df

def uniteDatetimeShape(df, datetime_column= 'ds', datetime_format= '%Y-%m-%d'):
    """
    datetime을 pd.to_datetime 코드로 처리할 때, datetime.strptime 코드로 처리할 때 각각
    Timestamp, datetime dtype로 바뀌는 문제가 나타났습니다.
    이를 해결하기 위해 datetime의 type을 일정하게 유지하도록 합니다.
    """
    df[datetime_column]= pd.to_datetime(
        df[datetime_column], box=True, format= datetime_format, exact=True)

def isDatetimeContinuous(df, datetime_column= 'ds'):
    #TODO
    return None

    
# Main #########################################################################

if __name__== '__main__':
    pass
