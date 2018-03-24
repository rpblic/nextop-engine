import unittest
import pandas as pd
import data, case, feature, IO, result, varr, visualization, table
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



class DataTest(unittest.TestCase):
    def setUp(self):
        self.dataclass= data.Data(df, 'test')
        self.dataclass.addMultipleXColAttribute(['ds','temp','rain'])



    def test_init(self):
        self.assertEqual(
            self.dataclass[testcase].loc[0,'ds'],
            df.loc[0,'ds']
            )

    def test_addData(self):
        self.dataclass.addDF(df2, 'test2')
        self.assertEqual(
            self.dataclass[testcase2].loc[0, 'ds'],
            df2.loc[0, 'ds']
            )

    def test_copyDatafrom(self):
        self.dataclass.copyDFfrom(testcase2, testcase)
        self.assertEqual(
            self.dataclass[testcase2].loc[0, 'ds'],
            self.dataclass[testcase].loc[0, 'ds']
            )

    def test_copyDatafrom_unrelated(self):
        self.dataclass.copyDFfrom(testcase2, testcase)
        self.dataclass[testcase2].loc[0, 'ds']= '2011-01-01'
        self.assertNotEqual(
            self.dataclass[testcase2].loc[0, 'ds'],
            self.dataclass[testcase].loc[0, 'ds']
            )

    def test_cases(self):
        self.assertTrue(testcase in self.dataclass.cases)

    def test_choosenCases_onecase(self):
        self.assertEqual(
            self.dataclass.choosenCases(testcase),
            [testcase]
            )

    def test_choosenCases_none(self):
        self.assertEqual(
            self.dataclass.choosenCases(None),
            self.dataclass.cases
            )

    def test_choosenCases_multiplecases(self):
        self.assertEqual(
            self.dataclass.choosenCases(['test', 'test2']),
            list()
            )

    def test_changeColumnNameforCases(self):
        self.dataclass.changeColumnNameforCases({'ds': 'day'})
        self.assertEqual(
            self.dataclass[testcase].columns.values.tolist(),
            ['day', 'y', 'y2', 'temp', 'rain']
            )

    def test_changeColumnNameforCases_errorcase(self):
        self.assertRaises(
            ValueError,
           self.dataclass.changeColumnNameforCases({'일자': 'day'})
            )

    def test_restructCasebyOneFeature_colname(self):
        self.dataclass= data.Data(df_preprocessing, 'test')
        self.dataclass.restructCasebyOneFeature(
            testcase, 'ds', 'ft', 'val')
        self.assertEqual(
            set(self.dataclass[testcase].columns.values.tolist()),
            {'ds', 'y', 'y2'}
            )

    def test_restructCasebyOneFeature_element(self):
        self.dataclass= data.Data(df_preprocessing, 'test')
        self.dataclass.restructCasebyOneFeature(
            testcase, 'ds', 'ft', 'val')
        self.assertEqual(
            self.dataclass[testcase].y.tolist(),
            df.y.tolist()
            )

    def test_divideCasebyColumns_colname(self):
        self.dataclass.divideCasebyColumns(inputcase= testcase)
        testcase_withy= case.addCaseProperty(testcase, 'y')
        self.assertEqual(
            set(self.dataclass[testcase_withy].columns.values.tolist()),
            {'ds', 'y', 'temp', 'rain'}
            )

    def test_divideCasebyColumns_element(self):
        self.dataclass.divideCasebyColumns(inputcase= testcase)
        testcase_withy= case.addCaseProperty(testcase, 'y2')
        self.assertEqual(
            self.dataclass[testcase_withy].loc[0, 'y2'],
            df.loc[0, 'y2']
            )

    def test_divideCasebyValueCondition(self):
        dict_of_condition= {'under100000': {50000},
                            'over100000': {100000, 150000}}
        self.dataclass.divideCasebyValueCondition(
            inputcase= testcase, dict_of_condition= dict_of_condition, name= 'y')
        test_div= case.addCaseProperty(testcase, 'y')
        test_div= case.addCaseProperty(test_div, 'under100000')
        self.assertEqual(
            self.dataclass[test_div].ds.tolist(),
            ['2010-01-02', '2010-01-03',]
            )

    def test_uniqueCondition(self):
        dict_of_condition= self.dataclass.uniqueCondition(
            self.dataclass[testcase].y)
        self.dataclass.divideCasebyValueCondition(
            inputcase= testcase, dict_of_condition= dict_of_condition, name= 'y')
        test_div= case.addCaseProperty(testcase, 'y')
        test_div= case.addCaseProperty(test_div, '100000_in_3')
        self.assertEqual(
            self.dataclass[test_div].ds.tolist(),
            ['2010-01-01', '2010-01-05',]
            )

    def test_divideCasebyCycle(self):
        self.dataclass.divideCasebyCycle(
            testcase, 3, 'test_cycle')
        test_div= case.addCaseProperty(testcase, 'test_cycle')
        test_div= case.addCaseProperty(test_div, '0_in_3')
        self.assertEqual(
            self.dataclass[test_div].ds.tolist(),
            ['2010-01-01', '2010-01-04',]
            )

    def test_divideCasebyPeriod(self):
        self.dataclass.divideCasebyPeriod(
            testcase, 3, 'test_period', start_num= 1)
        test_div= case.addCaseProperty(testcase, 'test_period')
        test_div= case.addCaseProperty(test_div, '1_in_2')
        self.assertEqual(
            self.dataclass[test_div].ds.tolist(),
            ['2010-01-03', '2010-01-04', '2010-01-05',]
            )

class TableTest(unittest.TestCase):
    def setUp(self):
        df_datetimeshape= df.copy()
        feature.uniteDatetimeShape(df_datetimeshape, datetime_format= '%Y-%m-%d')
        self.dataclass= data.Data(df_datetimeshape, 'test')
        self.dataclass.addMultipleXColAttribute(['ds','temp','rain'])
        self.table= self.dataclass[testcase]
        self.table.addDFCase(self.dataclass, testcase, forecastday= 2)

    def test_init(self):
        self.assertEqual(
            self.table.shape,
            (5,5)
            )

    def test_y_col(self):
        self.assertEqual(
            set(self.table.y_col),
            {'y', 'y2'}
            )

    def test_y_columnname(self):
        self.table= data.Table(self.table[['ds', 'y']])
        self.table.addDFCase(self.dataclass, testcase)
        self.assertEqual(
            self.table.y_columnname,
            'y'
            )

    def test_y_columnname_atterr(self):
        self.assertEqual(
            self.table.isYUnique(),
            False
            )

    def test_x_col(self):
        self.assertEqual(
            set(self.table.x_col),
            {'ds', 'temp', 'rain'}
            )

    def test_last_date(self):
        self.assertEqual(
            self.table.last_date.strftime(format= '%Y-%m-%d'),
            '2010-01-05'
            )

    def test_XX(self):
        self.assertEqual(
            self.table.XX.shape,
            (5, 3)
            )

    def test_YY(self):
        self.assertEqual(
            self.table.YY.shape,
            (5, 2)
            )

    def test_trainX(self):
        self.assertEqual(
            self.table.trainX.shape,
            (3, 3)
            )

    def test_testY(self):
        self.assertEqual(
            self.table.testY.shape,
            (2,2)
            )

class CaseTest(unittest.TestCase):
    def setUp(self):
        self.aCase= case.Case([])
        self.bCase= case.Case([1,2,3,4])
        self.cCase= case.Case([1,3])
        self.cases= {self.aCase: 'a', self.bCase: 'b', self.cCase: 'c'}

    def test_addCaseProperty_notiter(self):
        self.assertEqual(
            case.addCaseProperty(self.cCase, 4),
            case.Case([1,3,4])
            )

    def test_addCaseProperty_iter(self):
        self.assertEqual(
            case.addCaseProperty(self.cCase, [2,4]),
            self.bCase
            )

    def test_findCasePropertiesInData(self):
        self.assertEqual(
            case.findCasePropertiesInData([1], self.cases),
            [self.bCase, self.cCase]
            )

    def test_findCasePropertiesInData_none(self):
        self.assertEqual(
            case.findCasePropertiesInData([1, 5], self.cases),
            list()
            )

    # def test_print(self):

class FeatureTest(unittest.TestCase):
    pass

class IOTest(unittest.TestCase):
    def test_from_xlsx(self):
        testdf= IO.from_xlsx('KPP일별입고(13_17)_daily_obj.xlsx')
        self.assertEqual(
            testdf.columns.values.tolist(),
            ['ds', 1025, 1041, 1057, 1091, 1111, 1117, 1119, 1127, 1163, 1216, 1242,
            1261, 1298, 1355, 1373, 1375, 1376, 1390, 1396, 1627, 1652, 1656, 1692,
            1729, 1745, 1754, 1797, 1800, 1815, 1817, 1852, 1853, 1878, 1891, 'y_sum']
            )

    def test_to_xlsx(self):
        IO.to_xlsx(df, 'test.xlsx')
        testdf= IO.from_xlsx('test.xlsx')
        self.assertEqual(
            df.ds.tolist(),
            testdf.ds.tolist()
            )

    def test_from_pickle(self):
        testdf= IO.from_pickle('KPP일별회수(13_17)_daily_obj.pickle')
        self.assertEqual(
            testdf.iloc[0, 1:].tolist(),
            [0,81,0,0,0,0,0,0,0,584,0,0,0,0,0,28,0,0,0,0,
            7681,0,0,0,0,8374,0,0,0,0,0,0,0,0,0,0,0,0,0])

    def test_to_pickle(self):
        IO.to_pickle(df, 'test.pickle')
        testdf= IO.from_pickle('test.pickle')
        self.assertEqual(
            df.y.tolist(),
            testdf.y.tolist()
            )

class ResultTest(unittest.TestCase):
    pass

class VariablesTest(unittest.TestCase):
    pass

class VisualizationTest(unittest.TestCase):
    pass



if __name__== '__main__':
    TestList= {'data':DataTest,
                'table': TableTest,
                'case': CaseTest,
                'feature': FeatureTest,
                'io': IOTest,
                'result': ResultTest,
                'varr': VariablesTest,
                'visualization': VisualizationTest}
    test= TestList[sys.argv[1]]
    suite= unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity= 3).run(suite)