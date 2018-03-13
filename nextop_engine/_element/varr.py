import os
import sys
path_name= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

import pandas as pd
import pickle
from datetime import datetime, timedelta


PJ_DIR= path_name
TEMP_DATA_DIR= '\\_element\\data\\temp_data\\'
DF_DIR= '\\_element\\data\\data_in_use\\'
START_DATE= datetime(2010, 7, 1)
START_DATE_STR= START_DATE.strftime("%Y-%m-%d")
FORECASTDAY= 7
LAST_DATE= datetime(2017, 11, 30)
END_DATE= (LAST_DATE - timedelta(days=FORECASTDAY))
END_DATE_STR= END_DATE.strftime("%Y-%m-%d")



newyear = pd.DataFrame({
    'holiday': 'newyear',
    'ds': pd.to_datetime(['2011-02-03', '2012-01-23',
                          '2013-02-10', '2014-01-31', '2015-02-19',
                          '2016-02-09', '2017-02-28', '2018-02-16']),
    'lower_window': -4,
    'upper_window': 4,
})

newyearbefore = pd.DataFrame({
    'holiday': 'newyearbefore',
    'ds': pd.to_datetime(['2011-01-26', '2012-01-15',
                          '2013-02-02', '2014-01-23', '2015-02-11',
                          '2016-02-01', '2017-02-20', '2018-02-08']),
    'lower_window': -4,
    'upper_window': 4,
})

thanksgiving = pd.DataFrame({
    'holiday': 'thanksgiving',
    'ds': pd.to_datetime(['2010-09-22', '2011-09-12', '2012-09-30',
                          '2013-09-19', '2014-09-09', '2015-09-27',
                          '2016-09-15', '2017-10-04', '2018-09-24']),
    'lower_window': -4,
    'upper_window': 4,
})

thanksgivingbefore = pd.DataFrame({
    'holiday': 'thanksgivingbefore',
    'ds': pd.to_datetime(['2010-09-14', '2011-09-04', '2012-09-22',
                          '2013-09-11', '2014-09-01', '2015-09-19',
                          '2016-09-07', '2017-09-26', '2018-09-16']),
    'lower_window': -4,
    'upper_window': 4,
})

with open(PJ_DIR+TEMP_DATA_DIR+'reddays.pickle', 'rb') as f:
  reddaylist= pickle.load(f)
redday = pd.DataFrame({
  'holiday': 'redday',
  'ds': pd.to_datetime(reddaylist),
  'lower_window': -2,
  'upper_window': 2,
  })

# HOLYDAYBETA_old = pd.concat((newyear, thanksgiving, newyearbefore, thanksgivingbefore, redday))
HOLYDAYBETA = pd.concat((newyear, thanksgiving, redday))