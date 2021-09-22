from .riskiqapi import RiskIQAPI
import datetime

_ACTION_ = {'add':'ADD','remove':'REMOVE'}
_ALEXA_ = {'notinalexa':'NotRanked','top 100k':'Bucket1','top 10k':'Bucket0'}
_COLORS_ = {'yellow':'yellow', 'green':'green', 'orange':'orange', 'red':'red', 'purple':'purple', 'green-2':'green-2', 'dark-gray':'dark-grey', 'blue':'blue', 'black':'black', 'white':'white', 'indigo':'indigo', 'gray':'gray'}
_CONFIDENCE_ = {'absolute':'ABSOLUTE','high':'HIGH','low':'LOW','medium':'MEDIUM','unknown':'UNKNOWN','unlikely':'UNLIKELY'}
_DELTARANGE_ = {'1 day': 1,'7 days': 7,'30 days': 30,'1day': 1,'7days': 7,'30days': 30,1: 1,7: 7,30: 30}
_DOMAINEXPIRATION_ = {'expired':'Expired','expires in 30 days':'Expires30','expires in 60 days':'Expires60','expires in 90 days':'Expires90','expires in > 90 days':'ExpiresAfter90'}
_ENTERPRISE_ = {'true':True,'false':False}
_PORTLASTSEEN_ = {'7 days':7,'14 days':14,'30 days':30,'7days':7,'14days':14,'30days':30,7:7,14:14,30:30}
_PORTSTATE_ = {'filtered':'Filtered','open':'Open'}
_PRIORITY_ = {'high':'HIGH','low':'LOW','medium':'MEDIUM','none':'NONE'}
_REMOVEDSTATE_ = {'archived':'ARCHIVED','dismissed':'DISMISSED'}
_SSLCERTEXPIRATION_ = {'expired':'Expired','expires in 30 days':'Expires30','expires in 60 days':'Expires60','expires in 90 days':'Expires90','expires in > 90 days':'ExpiresAfter90'}
_STATE_ = {'approved inventory':'CONFIRMED','confirmed':'CONFIRMED','candidate':'CANDIDATE','dependencies':'ASSOCIATED_THIRDPARTY','monitor only':'ASSOCIATED_PARTNER','requires investigation':'CANDIDATE_INVESTIGATE'}
_ASSETTYPE_ = {'asn':'AS','contact':'CONTACT','domain':'DOMAIN','host':'HOST','ip address':'IP_ADDRESS','ip block':'IP_BLOCK','mail server':'MAIL_SERVER','name server':'NAME_SERVER','page':'PAGE','resource':'RESOURCE','ssl cert':'SSL_CERT'}
_UPDATETYPE_ = {'state':'state','status':'state','removedstate':'removedState','priority':'priority','enterprise':'enterprise','tag':'tag','brand':'brand','organization':'organization','primarycontact':'primaryContact','secondarycontact':'secondaryContact','externalid':'externalID','externalmetadata':'externalMetadata','note':'note'}
_VALIDATIONTYPE_ = {'domain':'DOMAIN_VALIDATION','extended':'EXTENDED_VALIDATION','organization':'ORGANIZATION_VALIDATION'}
_DATEFORMAT_ = '%Y-%m-%d'
_DATETIMEFORMAT_ = '%Y-%m-%d %H:%M:%S'


class Value(RiskIQAPI):

    def __init__(self, gi_api=None, value=None):
        self._gi_api = gi_api
        # common 
        self._alexaBucket = None
        self._assetType = None
        self._color = None
        self._confidence = None
        self._dateType = None
        self._datetimeType = None
        self._deltaRange = None
        self._domainExpiration = None
        self._portLastSeen = None
        self._portState = None
        self._priority = None
        self._removedState = None
        self._sslCertExiration = None
        self._state = None
        self._validationType = None
        self._rando = None
        self._value = value
        self._tag = None
        self._tagList = None
        self._brand = None
        self._brandList = None
        self._org = None
        self._orgList = None
        # update only
        self._action = None
        self._updateType = None
        self._enterprise = None
        self._externalID = None
        self._externalMetadata = None
        self._note = None
        self._primaryContact = None
        self._secondarContact = None
        self._stringType = None
        self._listType = None
        self._dictType = None
        self._assetNameTypeList = None

    @property
    def stringType(self):
        """
        String value input type validation
        Set with Value().stringType = yourString

        :returns: self._stringType
        """
        return self._stringType
    
    @stringType.setter
    def stringType(self, stringType):
        if type(stringType) != str:
            raise ValueError('must be of type(str)')
        self._stringType = stringType
        self._value = stringType

    @property
    def listType(self):
        """
        List value input type validation
        Set with Value().listType = yourList

        :returns: self._listType
        """
        return self._listType
    
    @listType.setter
    def listType(self, listType):
        if type(listType) != list:
            raise ValueError('must be of type(list)')
        self._listType = listType
        self._value = listType

    @property
    def dictType(self):
        """
        Dict value input type validation
        Set with Value().dictType = yourDict

        :returns: self._dictType
        """
        return self._dictType
    
    @dictType.setter
    def dictType(self, dictType):
        if type(dictType) != dict:
            raise ValueError('must be of type(dict)')
        self._dictType = dictType
        self._value = dictType

    @property
    def assetNameTypeList(self):
        """
        AssetNameTypeList value input type validation
        Set with Value().assetNameTypeList = yourAssetNameTypeList

        :returns: self._assetNameTypeList
        """
        return self._assetNameTypeList
    
    @assetNameTypeList.setter
    def assetNameTypeList(self, assetNameTypeList):
        if type(assetNameTypeList) != list:
            raise ValueError('assetNameTypeList must be type(list)')
        else:
            for a in assetNameTypeList:
                if type(a) != dict:
                    raise ValueError('assetNameTypeList must contain at least one dict with format of {"name":yourName,"type":yourType}')
                if 'name' not in a.keys() or 'type' not in a.keys():
                    raise ValueError('assetNameTypeList must contain at least one dict with format of {"name":yourName,"type":yourType}')
        self._assetNameTypeList = assetNameTypeList
        self._value = assetNameTypeList

    @property
    def tag(self):
        """
        Returns current tag
        Set with Value().tag = yourtag
        Checks if requested invetory tag exists

        :returns: self._tag
        """
        return self._tag
    
    @tag.setter
    def tag(self, _tag):
        if self._tagList is None:
            self._tagList = get_tags(self)
        
        if type(_tag) is not list and type(_tag) is not str:
            raise TypeError('tag must be type str or type list')
        
        if type(_tag) is list:
            for t in _tag:
                if t not in list(self._tagList.keys()):
                    raise ValueError('{0} not a current tag - must be in: {1}'.format(t, list(self._tagList.keys())))
        else:
            if _tag not in list(self._tagList.keys()):
                raise ValueError('{0} not a current tag - must be in: {1}'.format(_tag, list(self._tagList.keys()))) 

        if type(_tag) is list:
            this_tag = []
            for t in _tag:
                for k, v in self._tagList.items():
                    if t == k:
                        this_tag.append(v)
            self._value = this_tag
            self._tag = this_tag
        else:
            for k, v in self._tagList.items():
                if _tag == k:
                    self._value = v
                    self._tag = v

    @property
    def brand(self):
        """
        Returns current brand
        Set with Value().brand = yourbrand
        Checks if requested brand tag exists

        :returns: self._brand
        """
        return self._brand
    
    @brand.setter
    def brand(self, _brand):
        if self._brandList is None:
            self._brandList = get_brands(self)
        
        if type(_brand) is not list and type(_brand) is not str:
            raise TypeError('brand must be type str or type list')
        
        if type(_brand) is list:
            for b in _brand:
                if b not in list(self._brandList.keys()):
                    raise ValueError('{0} not a current brand - must be in: {1}'.format(b, list(self._brandList.keys())))
        else:
            if _brand not in list(self._brandList.keys()):
                raise ValueError('{0} not a current brand - must be in: {1}'.format(_brand, list(self._brandList.keys()))) 

        if type(_brand) is list:
            this_brand = []
            for b in _brand:
                for k, v in self._brandList.items():
                    if b == k:
                        this_brand.append(v)
            self._value = this_brand
            self._brand = this_brand
        else:
            for k, v in self._brandList.items():
                if _brand == k:
                    self._value = v
                    self._brand = v

    @property
    def organization(self):
        """
        Returns current organization
        Set with Value().organization = yourorganization
        Checks if requested organization tag exists

        :returns: self._organization
        """
        return self._organization
    
    @organization.setter
    def organization(self, _org):
        if self._orgList is None:
            self._orgList = get_orgs(self)
        
        if type(_org) is not list and type(_org) is not str:
            raise TypeError('organization must be type str or type list')
        
        if type(_org) is list:
            for o in _org:
                if o not in list(self._orgList.keys()):
                    raise ValueError('{0} not a current organization - must be in: {1}'.format(o, list(self._orgList.keys())))
        else:
            if _org not in list(self._orgList.keys()):
                raise ValueError('{0} not a current organization - must be in: {1}'.format(_org, list(self._orgList.keys()))) 

        if type(_org) is list:
            this_org = []
            for o in _org:
                for k, v in self._orgList.items():
                    if o == k:
                        this_org.append(v)
            self._value = this_org
            self._org = this_org
        else:
            for k, v in self._orgList.items():
                if _org == k:
                    self._value = v
                    self._org = v

    @property
    def dateType(self):
        """
        Returns current Date Value
        Set with Value().dateType = yourdateType

        :returns: self._dateType
        """
        return self._dateType
    
    @dateType.setter
    def dateType(self, dateType):
        try:
            datetime.datetime.strptime(dateType, _DATEFORMAT_)
            self._dateType = dateType
            self._value = dateType
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")

    @property
    def datetimeType(self):
        """
        Returns current Date Value
        Set with Value().datetimeType = yourdatetimeType

        :returns: self._datetimeType
        """
        return self._datetimeType
    
    @datetimeType.setter
    def datetimeType(self, datetimeType):
        try:
            datetime.datetime.strptime(datetimeType, _DATETIMEFORMAT_)
            self._datetimeType = datetimeType
            self._value = datetimeType
        except ValueError:
            raise ValueError("Incorrect datetime format, should be YYYY-MM-DD HH:MM:SS")

    @property
    def value(self):
        """
        Returns current value
        Set with Value().value = yourvalue

        :returns: self._value
        """
        return self._value
    
    @value.setter
    def value(self, _value):
        self._value = _value

    @property
    def rando(self):
        return self._rando
    
    @rando.setter
    def rando(self, rando):
        self._rando = rando
        self._value = rando

    @property
    def action(self):
        """
        Returns current action
        Set with Value().action = youraction

        :returns: self._action
        """
        return self._action

    @action.setter
    def action(self, action):
        if input_validation('action', _ACTION_, action):
            self._action = value_setter(_ACTION_, action)
            self._value = value_setter(_ACTION_, action)

    @property
    def alexaBucket(self):
        """
        Returns current alexaBucket
        Set with Value().alexaBucket = youralexaBucket

        :returns: self._alexaBucket
        """
        return self._alexaBucket

    @alexaBucket.setter
    def alexaBucket(self, alexaBucket):
        if input_validation('alexaBucket', _ALEXA_, alexaBucket):
            self._alexaBucket = value_setter(_ALEXA_, alexaBucket)
            self._value = value_setter(_ALEXA_, alexaBucket)

    @property
    def assetType(self):
        """
        Returns current assetType
        Set with Value().assetType = yourassetType

        :returns: self._assetType
        """
        return self._assetType

    @assetType.setter
    def assetType(self, assetType):
        if input_validation('assetType', _ASSETTYPE_, assetType):
            this_v = value_setter(_ASSETTYPE_, assetType)
            self._assetType = this_v
            self._value = this_v
    
    @property
    def updateType(self):
        """
        Returns current updateType
        Set with Value().updateType = yourupdateType

        :returns: self._updateType
        """
        return self._updateType

    @updateType.setter
    def updateType(self, updateType):
        if input_validation('updateType', _UPDATETYPE_, updateType):
            this_v = value_setter(_UPDATETYPE_, updateType)
            self._updateType = this_v
            self._value = this_v

    @property
    def color(self):
        """
        Returns current color
        Set with Value().color = yourcolor

        :returns: self._color
        """
        return self._color

    @color.setter
    def color(self, color):
        if input_validation('color', _COLORS_, color.lower()):
            this_v = value_setter(_COLORS_, color.lower())
            self._color = this_v
            self._value = this_v
    

    @property
    def confidence(self):
        """
        Returns current confidence
        Set with Value().confidence = yourconfidence

        :returns: self._confidence
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        if input_validation('confidence', _CONFIDENCE_, confidence):
            this_v = value_setter(_CONFIDENCE_, confidence)
            self._confidence = this_v
            self._value = this_v
            
    @property
    def deltaRange(self):
        """
        Returns current deltaRange
        Set with Value().pdeltaRange = deltaRange

        :returns: self._deltaRange
        """
        return self._deltaRange

    @deltaRange.setter
    def deltaRange(self, deltaRange):
        if input_validation('deltaRange', _DELTARANGE_, deltaRange):
            this_v = value_setter(_DELTARANGE_, deltaRange)
            self._deltaRange = this_v
            self._value = this_v

    @property
    def domainExpiration(self):
        """
        Returns current domainExpiration
        Set with Value().brand = yourdomainExpiration

        :returns: self._domainExpiration
        """
        return self._domainExpiration

    @domainExpiration.setter
    def domainExpiration(self, domainExpiration):
        if input_validation('domainExpiration', _DOMAINEXPIRATION_, domainExpiration):
            this_v = value_setter(_DOMAINEXPIRATION_, domainExpiration)
            self._domainExpiration = this_v
            self._value = this_v

    @property
    def portLastSeen(self):
        """
        Returns current portLastSeen
        Set with Value().portLastSeen = yourportLastSeen

        :returns: self._portLastSeen
        """
        return self._portLastSeen

    @portLastSeen.setter
    def portLastSeen(self, portLastSeen):
        if input_validation('portLastSeen', _PORTLASTSEEN_, portLastSeen):
            this_v = value_setter(_PORTLASTSEEN_, portLastSeen)
            self._portLastSeen = this_v
            self._value = this_v

    @property
    def portState(self):
        """
        Returns current portState
        Set with Value().portState = yourportState

        :returns: self._portState
        """
        return self._portState

    @portState.setter
    def portState(self, portState):
        if input_validation('portState', _PORTSTATE_, portState):
            this_v = value_setter(_PORTSTATE_, portState)
            self._portState = this_v
            self._value = this_v

    @property
    def priority(self):
        """
        Returns current priority
        Set with Value().priority = yourpriority

        :returns: self._priority
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        if input_validation('priority', _PRIORITY_, priority):
            this_v = value_setter(_PRIORITY_, priority)
            self._priority = this_v
            self._value = this_v

    @property
    def removedState(self):
        """
        Returns current removedState
        Set with Value().removedState = yourremovedState

        :returns: self._removedState
        """
        return self._removedState

    @removedState.setter
    def removedState(self, removedState):
        if input_validation('removedState', _REMOVEDSTATE_, removedState):
            this_v = value_setter(_REMOVEDSTATE_, removedState)
            self._removedState = this_v
            self._value = this_v
            
    @property
    def sslCertExpiration(self):
        """
        Returns current sslCertExpiration
        Set with Value().sslCertExpiration = yoursslCertExpiration

        :returns: self._sslCertExpiration
        """
        return self._sslCertExpiration

    @sslCertExpiration.setter
    def sslCertExpiration(self, sslCertExpiration):
        if input_validation('sslCertExpiration', _SSLCERTEXPIRATION_, sslCertExpiration):
            this_v = value_setter(_SSLCERTEXPIRATION_, sslCertExpiration)
            self._sslCertExpiration = this_v
            self._value = this_v

    @property
    def state(self):
        """
        Returns current state
        Set with Value().state = yourstate

        :returns: self._state
        """
        return self._state

    @state.setter
    def state(self, state):
        if input_validation('state', _STATE_, state):
            this_v = value_setter(_STATE_, state)
            self._state = this_v
            self._value = this_v

    @property
    def validationType(self):
        """
        Returns current validationType
        Set with Value().validationType = yourvalidationType

        :returns: self._validationType
        """
        return self._validationType

    @validationType.setter
    def validationType(self, validationType):
        if input_validation('validationType', _VALIDATIONTYPE_, validationType):
            this_v = value_setter(_VALIDATIONTYPE_, validationType)
            self._validationType = this_v
            self._value = this_v
        
    @property
    def enterprise(self):
        """
        Returns current enterprise
        Set with Value().enterprise = yourenterprise

        :returns: self._enterprise
        """
        return self._enterprise
    
    @enterprise.setter
    def enterprise(self, enterprise):
        if input_validation('enterprise', _ENTERPRISE_, enterprise):
            this_v = value_setter(_ENTERPRISE_, enterprise)
            self._enterprise = this_v
            self._value = this_v
    
    @property
    def externalID(self):
        """
        Returns current externalID
        Set with Value().externalID = yourexternalID

        :returns: self._externalID
        """
        return self._externalID
    
    @externalID.setter
    def externalID(self, externalID):
        self._externalID = externalID
        self._value = externalID

    @property
    def externalMetadata(self):
        """
        Returns current externalMetadata
        Set with Value().externalMetadata = yourexternalMetadata

        :returns: self._externalMetadata
        """
        return self._externalID
    
    @externalMetadata.setter
    def externalMetadata(self, externalMetadata):
        self._externalMetadata = externalMetadata
        self._value = externalMetadata
    
    @property
    def note(self):
        """
        Returns current note
        Set with Value().note = yournote

        :returns: self._note
        """
        return self._note

    @note.setter
    def note(self, note):
        self._note = note
        self._value = note

    @property
    def primaryContact(self):
        """
        Returns current primaryContact
        Set with Value().primaryContact = yourprimaryContact

        :returns: self._primaryContact
        """
        return self._primaryContact

    @primaryContact.setter
    def primaryContact(self, primaryContact):
        self._primaryContact = primaryContact
        self._value = primaryContact

    @property
    def secondaryContact(self):
        """
        Returns current secondaryContact
        Set with Value().secondaryContact = yoursecondaryContact

        :returns: self._secondaryContact
        """
        return self._secondaryContact

    @secondaryContact.setter
    def secondaryContact(self, secondaryContact):
        self._secondaryContact = secondaryContact
        self._value = secondaryContact

    def get_attr(self):
        return []

def input_validation(this_facet, facet_dict, value):
    if type(value) == list:
        for t in value:
            if type(t) is not int:
                if t.lower() not in list(facet_dict.keys()):
                    raise ValueError('{0} must be in: {1}'.format(this_facet, list(facet_dict.keys())))
            else:
                if t not in list(facet_dict.keys()):
                    raise ValueError('{0} must be in: {1}'.format(this_facet, list(facet_dict.keys())))
    elif type(value) == int:
        if value not in list(facet_dict.keys()):
            raise ValueError('{0} must be in: {1}'.format(this_facet, list(facet_dict.keys())))
    else:
        if value.lower() not in list(facet_dict.keys()):
            raise ValueError('{0} must be in: {1}'.format(this_facet, list(facet_dict.keys())))  
    return True

def value_setter(this_facet, value):
    if type(value) == list:
        this_l = []
        for t in value:
            for k,v in this_facet.items():
                if type(t) is not int:
                    if t.lower() == k:
                        this_l.append(v)
                else:
                    if t == k:
                        this_l.append(v)
        this_value = this_l
    else:
        for k,v in this_facet.items():
            if type(value) == str:
                if value.lower() == k:
                    this_value = v
            elif type(value) == int:
                if value == k:
                    this_value = v
            else:
                raise TypeError('{0} is unexpectd type: {1}'.format(value, type(value)))
    return this_value

def get_tags(self):
    tagList = self._gi_api.get('tags')
    this_tagList = {}
    for t in tagList.json():
        this_tagList.update({t['name']:t['id']})
    return this_tagList

def get_brands(self):
    brandList = self._gi_api.get('brands')
    this_brandList = {}
    for b in brandList.json():
        this_brandList.update({b['name']:b['id']})
    return this_brandList

def get_organizations(self):
    orgList = self._gi_api.get('organizations')
    this_orgList = {}
    for o in orgList.json():
        this_orgList.update({o['name']:o['id']})
    return this_orgList