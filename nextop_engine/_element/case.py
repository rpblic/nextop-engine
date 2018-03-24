class Case(frozenset):
    def edit(self):
        #TODO
        return None

def makeCasebyProperty(inputproperty):
    if isiterable(inputproperty):
        return Case(inputproperty)
    else:
        return Case((inputproperty, ))

def isiterable(x):
    try:
        if type(x) != type('str'):
            return bool(iter(x))
    except TypeError:
        pass
    return False



def addCaseProperty(case, addon_property):
    addon_case= makeCasebyProperty(addon_property)
    return case.copy().union(addon_case)

def removeCaseProperty(case, del_property):
    del_case= makeCasebyProperty(del_property)
    return case.copy().difference(del_case)



def findCasePropertiesInData(casename, data):
    cases= list(data.keys())
    return [case for case in cases
            if isincluded(casename, case)]

def isincluded(casename, case):
    casename_frozenset= makeCasebyProperty(casename)
    return casename_frozenset.issubset(case)



def deleteCaseFrom(casename, data):
    for case in data.cases:
        if isincluded(casename, case):
            data.pop(case, None)



def dividedCase(case, addon_property, del_property= None):
    if isiterable(addon_property):
        if del_property:
            case.removeCaseProperty(case, del_property)
        return divideMultipleCase(case, addon_property)
    else:
        return addCaseProperty(case, addon_property)        

def dividedMultipleCase(case, addon_cases):
    resultcases= []
    for addon_case in addon_cases:
        resultcases.append(addCaseProperty(case, addon_case))
    return resultcases



