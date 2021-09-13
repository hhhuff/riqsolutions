
_COMPARATORS_ = {
    'equals':'EQ',
    '=':'EQ',
    'notEquals':'NE',
    '!=':'NE',
    '_in':'IN',
    'notIn':'NOT_IN',
    'matches':'MATCHES',
    'notMatches':'NOT_MATCHES',
    'matchesIn':'MATCHES_IN',
    'notMatchesIn':'NOT_MATCHES_IN',
    'startsWith':'STARTS_WITH',
    'doesNotStartWith':'NOT_STARTS_WITH',
    'startsWithIn':'STARTS_WITH_IN',
    'doesNotStartWithIn':'NOT_STARTS_WITH_IN',
    'contains':'CONTAINS',
    'notContains':'NOT_CONTAINS',
    'containsIn':'CONTAINS_IN',
    'notContainsIn':'NOT_CONTAINS_IN',
    'empty':'NULL',
    'notEmpty':'NOT_NULL',
    'greaterThanOrEqualTo':'GTE',
    '>=':'GTE',
    'lessThanOrEqualTo':'LTE',
    '>=':'LTE',
    'between':'BETWEEN'
}

class Comparator():
    equals = 'equals'
    notEquals = 'notEquals'
    _in = '_in'
    notIn = 'notIn'
    matches = 'matches'
    notMatches = 'notMatches'
    matchesIn = 'matchesIn'
    notMatchesIn = 'notMatchesIn'
    startsWith = 'startsWith'
    doesNotStartWith = 'doesNotStartWith'
    startsWithIn = 'startsWithIn'
    doesNotStartWithIn = 'doesNotStartWithIn'
    contains = 'contains'
    notContains = 'notContains'
    containsIn = 'containsIn'
    notContainsIn = 'notContainsIn'
    empty = 'empty'
    notEmpty = 'notEmpty'
    greaterThanOrEqualTo = 'greaterThanOrEqualTo'
    lessThanOrEqualTo = 'lessThanOrEqualTo'
    between = 'between'
    
    def __init__(self):
        self._comparator = None

    @property
    def comparator(self):
        return self._comparator
    
    @comparator.setter
    def comparator(self, value):
        if type(value) is not str:
            raise TypeError('comparator {0} value must be type: str'.format(value,))
        comparator_list = [c.lower() for c in list(_COMPARATORS_.keys())]
        if value.lower() not in comparator_list:
            raise ValueError('{0} must be in: {1}'.format(value, list(_COMPARATORS_.keys())))
        for k, v in _COMPARATORS_.items():
            if value.lower() == k.lower():
                self._comparator = v

    def get_comparators(self):
        return list(_COMPARATORS_.keys())
