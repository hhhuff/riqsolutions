from .riskiqapi import RiskIQAPI
from riqsolutions.riskiqapi.workspace import Workspace
from riqsolutions.cli import configure_api
import re
import json


class Query(RiskIQAPI):
    def __init__(self, api_token=None, api_key=None):
        super().__init__(
            api_token, 
            api_key, 
            url_prefix='v1/globalinventory', 
            hostname='api.riskiq.net'
            )
        self._fullQuery=[]
        self._EC = 0
        self._tagList = tag_list()
        self._brandList = brand_list()
        self._orgList = org_list()

    def get_query(self):
        return self._fullQuery
    
    def get_tags(self):
        return self._tagList
    
    def get_brands(self):
        return self._brandList
    
    def get_organizations(self):
        return self._orgList

    def add(self, facet=None, comparator=None, value=None):
        this_value = value
        if facet == 'tag':
            this_value = check_values(self, 'tag', this_value)
        if facet == 'brand':
            this_value = check_values(self, 'brand', this_value)
        if facet == 'organization':
            this_value = check_values(self, 'org', this_value)

        self._EC += 1
        self._fullQuery.append(
            {'expressionId':self._EC,'operator':'and','facet':facet,'comparator':comparator,'value':this_value}
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
                
            
    def run(self, size=1000, page=0):
        """
        https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_search
        query: type(json) - required
        global: type(bool) - optional (default: False) << don't make available?
        size: type(int) - optional (default: 100)
        page: type(int) - optional (default: 0)
        """
        this_payload = process_query_object(self)
        print(json.dumps(this_payload, indent=4))
        this_params = {
            'global':False,
            'size':size,
            'mark':'*',
            'idsOnly':True
        }
        r = self.post('search', payload=this_payload, params=this_params)
        return {'results':r}
    
def tag_list():
    this_self = Workspace()
    configure_api(this_self)
    r = this_self.get('tag')
    return r.json()

def brand_list():
    this_self = Workspace()
    configure_api(this_self)
    r = this_self.get('brand')
    return r.json()

def org_list():
    this_self = Workspace()
    configure_api(this_self)
    r = this_self.get('organization')
    return r.json()

def check_values(self, checkType, value):
    this_value = value
    if checkType == 'tag':
        this_list = self._tagList['tags']
    if checkType == 'brand':
        this_list = self._brandList['brands']
    if checkType == 'org':
        this_list = self._orgList['organizations']
    if type(value) is not list:
        chk_flag = False
        for t in this_list:
            if t['name'] == value:
                this_value = t['id']
                chk_flag = True
                break
        if chk_flag == False:
            raise TypeError("{0} - is not a current {1} Name".format(value, checkType))
    else:
        this_value = []
        for v in value:
            chk_flag = False
            for t in this_list:
                if t['name'] == v:
                    this_value.append(t['id'])
                    chk_flag = True
            if chk_flag == False:
                raise TypeError("{0} - is not a current {1} Name".format(value, checkType))
    return this_value

def process_query_object(self):
    values = []
    for e in self._fullQuery:
        this_o = ''

        if e['facet'] not in ['tag','brand','organization']:
            if type(e['value']) is not list:
                if re.match(r'(?i)approved inventory',e['value']):
                    e['value']= 'CONFIRMED'
            else:
                for v in ['value']:
                    if re.match(r'(?i)approved inventory',v):
                        v = 'CONFIRMED'
        
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
