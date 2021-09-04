class Comparators:
    def __init__(self):
        pass
    
    
    def get_all(self):
        return ['equals','notEquals','in','notIn','matches','notMatches','matchesIn','notMatchesIn','startsWith','doesNotStartWith','startsWithIn','doesNotStartWithIn','contains','notContains','containsIn','notContainsIn','empty','notEmpty','greaterThanOrEqualTo','lessThanOrEqualTo']
    
    equals = 'EQ'
    notEquals = 'NE'
    _in = 'IN'
    notIn = 'NOT_IN'
    matches = 'MATCHES'
    notMatches = 'NOT_MATCHES'
    matchesIn = 'MATCHES_IN'
    notMatchesIn = 'NOT_MATCHES_IN'
    startsWith = 'STARTS_WITH'
    doesNotStartWith = 'NOT_STARTS_WITH'
    startsWithIn = 'STARTS_WITH_IN'
    doesNotStartWithIn = 'NOT_STARTS_WITH_IN'
    contains = 'CONTAINS'
    notContains = 'NOT_CONTAINS'
    containsIn = 'CONTAINS_IN'
    notContainsIn = 'NOT_CONTAINS_IN'
    empty = 'NULL'
    notEmpty = 'NOT_NULL'
    greaterThanOrEqualTo = 'GTE'
    lessThanOrEqualTo = 'LTE'
