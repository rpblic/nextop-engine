import os
import sys
path_name = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from _element import case

class PredictionCases(dict):
    def __init__(self):
        self.result= dict()
        self.score= dict()

    def addModel(self, model, casename):
        case_by_frozenset= case.makeCasebyProperty(casename)
        self[case_by_frozenset]= model
        self.result[case_by_frozenset]
        self.score[case_by_frozenset]
        return None