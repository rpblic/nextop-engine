import unittest
import pandas as pd
import data, case
import sys


df= pd.DataFrame.from_items([
            ('ds', ['2010-01-01', '2010-01-02', '2010-01-03', '2010-01-04', '2010-01-05', ]),
            ('y', [100000, 50000, 50000, 150000, 100000, ]),
            ('y2', [0, 50000, 20000, 0, 0, ]),
            ('temp', ['10', '5', '10', '15', '5', ]),
            ('rain', ['0', '10', '0', '0', '0', ]),
            ])

df2= pd.DataFrame.from_items([
            ('ds', ['2011-01-01', '2011-01-02', '2011-01-03', '2011-01-04', '2011-01-05', ]),
            ('y', [100000, 50000, 150000, 50000, 100000, ]),
            ('y2', [0, 0, 50000, 50000, 100000, ]),
            ('temp', ['10', '5', '5', '15', '15', ]),
            ('rain', ['0', '1', '0', '2', '0', ]),
            ])

df_preprocessing= pd.DataFrame.from_items([
            ('ds', ['2011-01-01', '2011-01-02', '2011-01-02',
                    '2011-01-02', '2011-01-03', '2011-01-03',
                    '2011-01-04', '2011-01-04', '2011-01-05',
                    '2011-01-05',]),
            ('val', [100000, 30000, 20000,
                    50000, 50000, 20000,
                    100000, 50000, 50000, 50000]),
            ('ft', ['y', 'y', 'y',
                    'y2', 'y', 'y2',
                    'y', 'y', 'y', 'y']),
            ])

testcase= case.Case(['test'])
testcase2= case.Case(['test2'])



class ArimaTest(unittest.TestCase):
    pass

class ProphetTest(unittest.TestCase):
    pass

class LSTMTest(unittest.TestCase):
    pass



if __name__== '__main__':
    TestList= [ArimaTest, ProphetTest, LSTMTest]
    print(TestList)
    test= TestList[int(sys.argv[1])]
    suite= unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity= 3).run(suite)