from .riskiqapi import RiskIQAPI
from riqsolutions.riskiqapi.workspace import Workspace
from riqsolutions.riskiqapi.facets import Facet
from riqsolutions.riskiqapi.comparators import Comparator
from riqsolutions.riskiqapi.values import Value
from riqsolutions.cli import configure_api
import json

class Query(RiskIQAPI):
    def __init__(self, api_token=None, api_key=None, proxy=None, context=None):
        super().__init__(
            api_token, 
            api_key, 
            proxy,
            context,
            url_prefix='v1/globalinventory', 
            hostname='api.riskiq.net'
            )
        self._fullQuery=[]
        self._EC = 0

    def get_query(self):
        return self._fullQuery

    def get_facets(self):
        this_f = Facet()
        return this_f.get_facets()
    
    def get_comparators(self):
        this_f = Comparator()
        return this_f.get_comparators()

    def add(self, facet=None, comparator=None, value=None):
        this_f = Facet()
        this_f.facet = facet

        this_c = Comparator()
        this_c.comparator = comparator

        this_v = Value()
        configure_api(this_v, context=self.get_context())
        if this_f.facet.lower() == 'alexabucket':
            this_v.alexaBucket = value
        elif this_f.facet.lower() in ['type','assettype']:
            this_v.assetType = value
        elif this_f.facet == 'brand':
            this_v.brand = value
        elif this_f.facet == 'confidence':
            this_v.confidence = value
        elif this_f.facet == 'domainExpiration':
            this_v.domainExpiration = value
        elif this_f.facet in ['org','organizatin']:
            this_v.org = value
        elif this_f.facet == 'portLastSeen':
            this_v.portLastSeen = value
        elif this_f.facet == 'portState':
            this_v.portState = value
        elif this_f.facet == 'priority':
            this_v.priority = value
        elif this_f.facet == 'removedState':
            this_v.removedState = value
        elif this_f.facet == 'sslCertExpiration':
            this_v.sslCertExpiration = value
        elif this_f.facet == 'state':
            this_v.state = value
        elif this_f.facet == 'tag':
            this_v.tag = value
        elif this_f.facet == 'validationType':
            this_v.validationType = value
        else:
            this_v.rando = value
        
        self._EC += 1
        self._fullQuery.append(
            {'expressionId':self._EC,'operator':'and','facet':this_f.facet,'comparator':this_c.comparator,'value':this_v.value}
        )
        
    
    def _and(self, facet=None, comparator=None, value=None):
        self._EC += 1
        self._fullQuery.append(
            {'expressionId':self._EC,'operator':'and','facet':facet,'comparator':comparator,'value':value}
        )
    
    def _or(self, facet=None, comparator=None, value=None):
        self._EC += 1
        self._fullQuery.append(
            {'expressionId':self._EC,'operator':'or','facet':facet,'comparator':comparator,'value':value}
        )

    def remove(self, id):
        if type(id) is not list:
            for e in self._fullQuery:
                if e['expressionId'] == id:
                    self._fullQuery.remove(e)
        else:
            for this_id in id:
                for e in self._fullQuery:
                    if e['expressionId'] == this_id:
                        self._fullQuery.remove(e)
                
            
    def run(self, size=1000, idsOnly=False, threadindex=None):
        """
        https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_search
        query: type(json) - required
        global: type(bool) - optional (default: False) << don't make available?
        size: type(int) - optional (default: 1000)
        idsOnly: type(bool) - optional (default: False)
        """
        this_payload = process_query_object(self)
        full_response = []
        this_mark = '*'
        while True:
            this_params = {
                'global':False,
                'size':size,
                'mark':this_mark,
                'idsOnly':idsOnly
            }
            r = self.post('search', payload=this_payload, params=this_params, threadindex=threadindex)
            if type(r) == list and 'error' in r.keys():
                this_e = {'error':str(e),'method':method,'payload':payload,'params':params,'elapsed':t1_stop-t1_start}
            else:
                this_data = r.json()
                for c in this_data.get('content'):
                    full_response.append(c)
                if this_data.get('last') != True:
                    this_mark = this_data.get('mark')
                else:
                    return {'results':full_response}
    
def check_values(self, facetType, value):
    this_value = value
    if facetType == 'tag':
        this_list = self._tagList['tags']
    elif facetType == 'brand':
        this_list = self._brandList['brands']
    elif facetType == 'org':
        this_list = self._orgList['organizations']
    
    if facetType in ['tag','brand','org']:
        if type(value) is list:
            this_value = []
            for v in value:
                chk_flag = False
                for t in this_list:
                    if t['name'] == v:
                        this_value.append(t['id'])
                        chk_flag = True
                if chk_flag == False:
                    raise TypeError('{0} - is not a current {1} Name'.format(value, facetType))
        else:
            chk_flag = False
            for t in this_list:
                if t['name'] == value:
                    this_value = t['id']
                    chk_flag = True
                    break
            if chk_flag == False:
                raise TypeError('{0} - is not a current {1} Name'.format(value, facetType))

    return this_value


def process_query_object(self):
    values = []
    for e in self._fullQuery:

        this_v = {
            'name':e['facet'],
            'operator':e['comparator'],
            'value':e['value']
        }
        values.append(this_v)

    this_payload = {
        'query':None,
        'filters': {
            'condition':'AND',
            'value':values
        }
    }
    return this_payload
