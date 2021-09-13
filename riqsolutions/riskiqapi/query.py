from .riskiqapi import RiskIQAPI
from riqsolutions.riskiqapi.workspace import Workspace
from riqsolutions.riskiqapi.facets import Facet
from riqsolutions.riskiqapi.comparators import Comparator
from riqsolutions.riskiqapi.values import Value
from riqsolutions.cli import configure_api
import json


# ALEXA = ['Not in Alexa','Top 100k','Top 10k']
# CONFIDENCE = ['Absolute','High','Low']
# DOMAINEXP = ['Expired','Expires in 30 days','Expires in 60 days','Expires in 90 days','Expires in > 90 days']
# PORTLASTSEEN = ['7 Days','14 Days','30 Days']
# PORTSTATE = ['Filtered','Open']
# PRIORITY = ['High','Low	Medium','None']
# REMOVEDSTATE = ['Archived','Dismissed']
# SSLCERTEXP = ['Expired','Expires in 30 days','Expires in 60 days','Expires in 90 days','Expires in > 90 days']
# STATE = ['Approved Inventory','Candidate','Dependencies','Monitor Only','Requires Investigation']
# _TYPE = ['ASN','Contact','Domain','Host','IP Address','IP Block','Mail Server','Name Server','Page','Resource','SSL Cert']
# VALIDATIONTYPE = ['Domain','Extended','Organization']
# FACETS = ['admin','adminEmail','adminOrg','alexaBucket','asnNumber','assetType','attributeType','attributeTypeValue','attributeValue','autoConfirmed','banner','bgpPrefix','brand','city','cname','cnameDomain','confidence','confidence','connected','country','countryCode','createdAt','cvss3BaseScore','cvssScore','cweID','discoveryRun','domainExpiration','domainStatus','email','enterprise','error','externalId','externalMetadata','finalResponseCode','finalScheme','finalUrl','firstSeen','hasMailServerRecord','hasNameServerRecord','ipv4','ipv6','issuerAlternativeName','issuerCommonName','keyAlgorithm','keySize','keystone','lastSeen','name','note','organization','parkedDomain','port','portLastSeen','portState','primaryContact','priority','regionCode','registrant','registrantEmail','registrantOrg','removedFromInventory','removedState','reputationType','resourceHost','resourceMd5','resourceUrl','scheme','secondarContact','securityPolicy','selfSigned','serialNumber','signatureAlgorithm','signatureAlgorithmOid','sslCertExpiration','sslCertIssuerOrganization','sslCertIssuerOrganizationalUnit','sslCertOrganization','sslCertOrganizationalUnit','sslCertSubjectOrganization','sslCertSubjectOrganizationalUnit','state','subjectAlternativeName','subjectCommonName','tag','techEmail','technical','technicalOrg','type','updatedAt','uuid','validationType','webComponentName','webComponentNameVersion','webComponentService','webComponentType','webComponentVersion','wildcard']

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
    
        # Facet.__init__()
        # Comparator.__init__()
        # Value.__init__()
        self._fullQuery=[]
        self._EC = 0
        # self._tagList = None
        # self._brandList = None
        # self._orgList = None

    def get_query(self):
        return self._fullQuery
    
    # def get_tags(self):
    #     if self._tagList == None:
    #         self._tagList = self.get('tags')
    #     return self._tagList
    
    # def get_brands(self):
    #     if self._brandList == None:
    #         self._brandList = self.get('brands')
    #     return self._brandList
    
    # def get_organizations(self):
    #     if self._orgList == None:
    #         self._orgList = self.get('organizations')
    #     return self._orgList

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
        


        # if facet == 'tag':
        #     if self._tagList == None:
        #         self._tagList = tag_list(self)
        #     value = check_values(self, 'tag', value)

        # if facet == 'brand':
        #     if self._brandList == None:
        #         self._brandList = brand_list()
        #     value = check_values(self, 'brand', value)

        # if facet == 'organization':
        #     if self._orgList == None:
        #         self._orgList = org_list()
        #     value = check_values(self, 'org', value)

        # if facet == 'alexaBucket':
        #     this_f = Value()
        #     this_f.alexaBucket(value)

        
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
                
            
    def run(self, size=1000, page=0, idsOnly=False):
        """
        https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_search
        query: type(json) - required
        global: type(bool) - optional (default: False) << don't make available?
        size: type(int) - optional (default: 100)
        page: type(int) - optional (default: 0)
        idsOnly: type(bool) - optional (default: False)
        """
        this_payload = process_query_object(self)
        this_params = {
            'global':False,
            'size':size,
            'mark':'*',
            'idsOnly':idsOnly
        }
        r = self.post('search', payload=this_payload, params=this_params)
        return {'results':r}
    
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

# def input_validation(facetType, value):
#     if facetType not in FACETS:
#         return {'input_check': False, 'err': 'Facet values must be in {0}'.format(FACETS)}

#     if facetType == 'alexaBucket':
#         if value in ALEXA:
#             return {'input_check': True, 'err':''}
#         else:
#             return {'input_check': False, 'err':'Alexa Rank Query values must be in {0}'.format(ALEXA)}

#     if facetType == 'assetType':
#         if value in _TYPE:
#             return {'input_check': True, 'err':''}
#         else:
#             return {'input_check': False, 'err':'Alexa Rank Query values must be in {0}'.format(_TYPE)}

#     if facetType == 'confidence':
#         if value in CONFIDENCE:
#             return {'input_check': True, 'err':''}
#         else:
#             return {'input_check': False, 'err':'Alexa Rank Query values must be in {0}'.format(CONFIDENCE)}

#     if facetType == 'domainExpiration':
#         if value in DOMAINEXP:
#             return {'input_check': True, 'err':''}
#         else:
#             return {'input_check': False, 'err':'Alexa Rank Query values must be in {0}'.format(DOMAINEXP)}

#     if facetType == 'portLastSeen':
#         if value in PORTLASTSEEN:
#             return {'input_check': True, 'err':''}
#         else:
#             return {'input_check': False, 'err':'Alexa Rank Query values must be in {0}'.format(PORTLASTSEEN)}

#     if facetType == 'portState':
#         if value in PORTSTATE:
#             return {'input_check': True, 'err':''}
#         else:
#             return {'input_check': False, 'err':'Alexa Rank Query values must be in {0}'.format(PORTSTATE)}

#     if facetType == 'priority':
#         if value in PRIORITY:
#             return {'input_check': True, 'err':''}
#         else:
#             return {'input_check': False, 'err':'Alexa Rank Query values must be in {0}'.format(PRIORITY)}

#     if facetType == 'removedState':
#         if value in REMOVEDSTATE:
#             return {'input_check': True, 'err':''}
#         else:
#             return {'input_check': False, 'err':'Alexa Rank Query values must be in {0}'.format(REMOVEDSTATE)}

#     if facetType == 'sslCertExpiration':
#         if value in SSLCERTEXP:
#             return {'input_check': True, 'err':''}
#         else:
#             return {'input_check': False, 'err':'Alexa Rank Query values must be in {0}'.format(SSLCERTEXP)}

#     if facetType == 'state':
#         if value in STATE:
#             return {'input_check': True, 'err':''}
#         else:
#             return {'input_check': False, 'err':'Alexa Rank Query values must be in {0}'.format(STATE)}

#     if facetType == 'validationType':
#         if value in VALIDATIONTYPE:
#             return {'input_check': True, 'err':''}
#         else:
#             return {'input_check': False, 'err':'Alexa Rank Query values must be in {0}'.format(VALIDATIONTYPE)}


def process_query_object(self):
    values = []
    for e in self._fullQuery:
        # this_o = ''

        # if e['facet'] in ['state','status']:
        #     if type(e['value']) is str:
        #         if re.match(r'(?i)approved inventory',e['value']):
        #             e['value']= 'CONFIRMED'
        #     elif type(e['value']) is list:
        #         for v in ['value']:
        #             if re.match(r'(?i)approved inventory',v):
        #                 v = 'CONFIRMED'

        #     if type(e['value']) is str:
        #         if re.match(r'(?i)candidate',e['value']):
        #             e['value']= 'CANDIDATE'
        #     elif type(e['value']) is list:
        #         for v in ['value']:
        #             if re.match(r'(?i)candidate',v):
        #                 v = 'CANDIDATE'

        #     if type(e['value']) is str:
        #         if re.match(r'(?i)dependencies',e['value']):
        #             e['value']= 'ASSOCIATED_THIRDPARTY'
        #     elif type(e['value']) is list:
        #         for v in ['value']:
        #             if re.match(r'(?i)dependencies',v):
        #                 v = 'ASSOCIATED_THIRDPARTY'
            
        #     if type(e['value']) is str:
        #         if re.match(r'(?i)monitor only',e['value']):
        #             e['value']= 'ASSOCIATED_PARTNER'
        #     elif type(e['value']) is list:
        #         for v in ['value']:
        #             if re.match(r'(?i)monitor only',v):
        #                 v = 'ASSOCIATED_PARTNER'

        #     if type(e['value']) is str:
        #         if re.match(r'(?i)requires investigation',e['value']):
        #             e['value']= 'CANDIDATE_INVESTIGATE'
        #     elif type(e['value']) is list:
        #         for v in ['value']:
        #             if re.match(r'(?i)requires investigation',v):
        #                 v = 'CANDIDATE_INVESTIGATE'

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
