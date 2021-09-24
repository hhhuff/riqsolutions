"""Global Inventory Module for the RiskIQ Solutions Python API Library"""

from .riskiqapi import RiskIQAPI
from .workspace import Workspace
from .values import Value
from riqsolutions.cli import configure_api
import json
import threading
from threading import Thread
import queue

QUEUE_LOCK = threading.Lock()

class GlobalInventory(RiskIQAPI):
    """
    Represents a request to the Global Inventory API
    https://api.riskiq.net/api/globalinventory/
    """
    def __init__(self, api_token=None, api_key=None, context=None):
        super().__init__(
            api_token, 
            api_key, 
            context,
            url_prefix='v1/globalinventory', 
            hostname='api.riskiq.net')
    

    def inventory_search(self, query: json=None, savedSearchID=None, savedSearchName=None, size: int=100, idsOnly=False):
        """
        Perform an inventory search by submitting json which was generated from the UI.

        https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_search

        :param query: type json, optional
        :param savedSearchId: type str, optional
        :param savedSarchName: type str, optional
        :param size: type int, optional (Default: 100)
        :param idsOnly: type bool, optional (Default: False)

        :returns: {'results':r}
        """
        this_params = {
            'global':False,
            'size':size,
            'mark':this_mark,
            'idsOnly':idsOnly
        }

        this_payload = None
        if query != None:
            _v = Value(self)
            _v.typeDict = query
            this_payload = _v.value
        elif savedSearchID != None:
            _s = Value(self)
            _s.stringType = savedSearchID
            this_params['savedSearchID'] = _s.value
        elif savedSearchName != None:
            _s = Value(self)
            _s.stringType = savedSearchName
            this_params['savedSearchName'] = _s.value

        full_response = []
        this_mark = '*'
        count=0
        while True:
            this_params['mark'] = this_mark
            r = self.post('search', payload=this_payload, params=this_params)
            if type(r) == dict and 'error' in r.keys():
                if count >= 5:
                    raise ValueError('GlobalInventory.inventory_search() failed too many times on the same mark bundle')
                else:
                    count += 1
            else:
                count = 0
                this_data = r.json()
                for c in this_data.get('content'):
                    full_response.append(c)
                if this_data.get('last') != True:
                    this_mark = this_data.get('mark')
                else:
                    return {'results':full_response}


    def get_asset_by_id(self, uuid: str=None, recent: bool=True):
        """
        Retrieve enrichment data for a single asset by its UUID.

        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_assets_id_uuid

        :param uuid: type str, required
        :param recent: type bool, optional
        :param global: type bool, optional
        """
        _v = Value(self)
        _v.stringType = uuid
        
        this_params = {
            'recent':recent,
            'global':False
        }

        r = self.get('assets/id/{}'.format(_v.value), params=this_params)
        return r.json()

    def get_asset(self, asset_name=None, asset_type=None, recent=True, size=100):
        """
        Retrieve enrichment data of a single asseet.

        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_assets_type

        :param asset_type: type str, required
        :param asset_name: type str, required
        :param recent: type bool, optional
        :param size: type int, optional
        """
        _an = Value(self)
        _an.stringType = asset_name

        this_params = {
            'name':_an.value,
            'recent':recent,
            'global':False,
            'size':size
        }

        _t = Value(self)
        _t.assetType = asset_type

        r = self.get('assets/{}'.format(_t.assetType.lower()), params=this_params)
        return r.json()

    def get_assets_bulk(self, asset_list:None, asset_type=None):
        """
        Retrieve encrichment data for a list of assets.

        https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_assets_bulk

        :param asset_type: type str, required
        :param asset_list: type list, required
        """
        _al = Value(self)
        _al.listType = asset_list

        _t = Value(self)
        _t.assetType = asset_type

        if len(_al.value) > 100:
            full_payload = bundler(endpoint='assets/bulk', payload=_al.value, asset_type=_t.assetType, bundle_size=10)
            _results = []
            while True:
                r = bulk_sequencer('assets/bulk', payload=full_payload, asset_type=_t.assetType, context=self.get_context(), max_thread_count=25)
                if len(r.get('resultList')) > 0:
                    for h in r.get('resultList'):
                        _results.append(h)
                if len(r.get('retryList')) > 0:
                    full_payload = bundler(endpoint='assets/bulk', payload=r.get('retryList'), asset_type=_t.assetType, bundle_size=10)
                else:
                    break
            return _results
        else:
            assets = []
            for a in _al.value:
                this_asset = {
                    "name": a,
                    "type": _t.assetType
                }
                assets.append(this_asset)
            this_payload = {
                'assets':assets
            }
            r = self.post('assets/bulk', payload=this_payload, asset_type=_t.assetType)
            return r
        

    def get_asset_attributes(self, asset_name=None, asset_type=None, recent=True, size=100):
        """
        Retrieve attributes enrichment data of a single asset.

        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_assets_type

        :param asset_type: type str, required
        :param asset_name: type str, required
        :param recent: type bool, optional (default: True)
        :param size: type int, optional (default: 100)
        """
        r = get_asset_dataset(self, 'attributes', asset_name, asset_type, recent, size)
        return {'results':r}

    def get_asset_cookies(self, asset_name=None, asset_type=None, recent=True, size=100):
        """
        Retrieve cookies enrichment data of a single asset.

        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_assets_type

        :param asset_type: type str, required
        :param asset_name: type str, required
        :param recent: type bool, optional (default: True)
        :param size: type int, optional (default: 100)
        """
        r = get_asset_dataset(self, 'cookies', asset_name, asset_type, recent, size)
        return {'results':r}

    def get_asset_hostpairs(self, asset_name=None, asset_type=None, recent=True, size=100):
        """
        Retrieve hostpairs enrichment data of a single asset.

        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_assets_type

        :param asset_type: type str, required
        :param asset_name: type str, required
        :param recent: type bool, optional (default: True)
        :param size: type int, optional (default: 100)
        """
        r = get_asset_dataset(self, 'hostPairs', asset_name, asset_type, recent, size)
        return {'results':r}

    def get_asset_minicrawls(self, asset_name=None, asset_type=None, recent=True, size=100):
        """
        Retrieve minicrawls enrichment data of a single asset.

        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_assets_type

        :param asset_type: type str, required
        :param asset_name: type str, required
        :param recent: type bool, optional (default: True)
        :param size: type int, optional (default: 100)
        """
        r = get_asset_dataset(self, 'miniCrawls', asset_name, asset_type, recent, size)
        return {'results':r}

    def get_asset_certificates(self, asset_name=None, asset_type=None, recent=True, size=100):
        """
        Retrieve certificates enrichment data of a single asset.

        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_assets_type

        :param asset_type: type str, required
        :param asset_name: type str, required
        :param recent: type bool, optional (default: True)
        :param size: type int, optional (default: 100)
        """
        r = get_asset_dataset(self, 'sslCerts', asset_name, asset_type, recent, size)
        return {'results':r}

    def get_asset_web_components(self, asset_name=None, asset_type=None, recent=True, size=100):
        """
        Retrieve web components enrichment data of a single asset.

        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_assets_type

        :param asset_type: type str, required
        :param asset_name: type str, required
        :param recent: type bool, optional (default: True)
        :param size: type int, optional (default: 100)
        """
        r = get_asset_dataset(self, 'webComponents', asset_name, asset_type, recent, size)
        return {'results':r}

    def get_asset_connected(self, asset_name=None, asset_type=None, recent=True, size=100, idsOnly=True, mark='*'):
        """
        Retrieve connected assets data of a single asset.

        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_assets_type

        :param asset_type: type str, required
        :param asset_name: type str, required
        :param recent: type bool, optional (default: True)
        :param size: type int, optional (default: 100)
        """
        _t = Value(self)
        _t.assetType = asset_type
         
        type_list= ['DOMAIN', 'HOST', 'PAGE', 'IP_BLOCK', 'IP_ADDRESS', 'CONTACT', 'SSL_CERT', 'AS']
        full_response = {'DOMAIN':[],'HOST':[],'PAGE':[],'IP_BLOCK':[],'IP_ADDRESS':[],'CONTACT':[],'SSL_CERT':[],'AS':[]}

        while True:
            more_flag = False
            this_params = {
                'name':asset_name,
                'global':False,
                'size':size,
                'page':0,
                'mark':mark,
                'idsOnly':idsOnly
            }
            r = self.get('assets/{0}/connected'.format(_t.assetType.lower()), params=this_params)
            this_data = r.json()
            for t in type_list:
                if t in this_data.keys():
                    if this_data.get(t)['last'] == False:
                        moreflag = True
                    if 'mark' in this_data.get(t).keys():
                        mark = this_data.get(t)['mark']
                    if len(this_data.get(t)['content']) > 0:
                        for c in this_data.get(t)['content']:
                            full_response.get(t).append(c)
            if moreflag != True:
                return full_response
            
    def get_asset_deltas(self, asset_type=None, date=None, delta_range=1, measure='ADDED', brand=None, organization=None, tag=None, size=100):
        """     
        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_deltas

        :param asset_type: type str, required
        :param date: type str, required (format: YYYY-MM-DD)
        :param delta_range: type int, optional must be 1, 7, or 30
        :param measure: type str, required
        :param brand: type str, optional
        :param organization: type str, optional
        :param tag: type str, optional
        :param size: type int, optional
        """

        _date = Value(self)
        _date.dateType = date

        _dr = Value(self)
        _dr.deltaRange = delta_range

        _t = Value(self)
        _t.assetType = asset_type

        if tag != None:
            _tag = Value(context=self.get_context())
            _tag.tag = tag
            tag = _tag.tag

        if brand != None:
            _brand = Value(context=self.get_context())
            _brand.brand = brand
            brand = _brand.brand

        if organization != None:
            _org = Value(context=self.get_context())
            _org.organization = organization
            organization = _org.organization

        full_response = []
        this_mark = '*'
        count=0
        while True:
            this_params = {
                'type': _t.assetType,
                'date': _date.value,
                'range': _dr.value,
                'measure': measure,
                'brand': brand,
                'organization': organization,
                'tag': tag,
                'size':size,
                'mark':this_mark
            }
            r = self.get('deltas', params=this_params)
            if type(r) == dict and 'error' in r.keys():
                if count >= 5:
                    raise ValueError('GlobalInventory.get_asset_deltas() failed too many times on the same mark bundle - Try an earlier date and/or a greater delta range')
                else:
                    count += 1
            else:
                count = 0
                this_data = r.json()
                for c in this_data.get('content'):
                    full_response.append(c)
                if this_data.get('last') != True:
                    this_mark = this_data.get('mark')
                else:
                    return {'results':full_response}


    def get_asset_deltas_summary(self, date=None, delta_range=1, brand=None, organization=None, tag=None, size=100):
        """     
        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_deltas_summary
        
        :param date: type str, required
        :param delta_range:  type int, optional must be 1, 7, or 30
        :param brand: type str, optional
        :param organization: type str, optional
        :param tag: type str, optional
        """

        _date = Value(self)
        _date.dateType = date

        _dr = Value(self)
        _dr.deltaRange = delta_range
        
        if tag != None:
            _tag = Value(context=self.get_context())
            _tag.tag = tag
            tag = _tag.tag

        if brand != None:
            _brand = Value(context=self.get_context())
            _brand.brand = brand
            brand = _brand.brand

        if organization != None:
            _org = Value(context=self.get_context())
            _org.organization = organization
            organization = _org.organization

        this_params = {
            'date': _date.value,
            'range': _dr.value,
            'brand': brand,
            'organization': organization,
            'tag': tag
        }

        r = self.get('deltas/summary', params=this_params)
        if type(r) == dict and 'error' in r.keys():
            raise ValueError(e)
        else:
            return r.json()
        
    def get_tasks(self):
        """
        Retrieve the status of all current tasks

        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_tasks
        """
        r = self.get('tasks')
        return r.json()

    def get_task(self, taskid=None):
        """
        Retrieve the status of a single task

        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_tasks

        :param taskid: type str, required
        """
        _t = Value(self)
        _t.stringType = taskid

        r = self.get('task/{0}'.format(_t.value))
        return r.json()
    
    def cancel_task(self, taskid=None):
        """
        Cancel a single task

        https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_task_id_cancel

        :param taskid: type str, required
        """
        _t = Value(self)
        _t.stringType = taskid

        r = self.post('task/{0}/cancel'.format(_t.value))
        return r.json()
        

    def get_tags(self):
        """
        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_tags
        """
        r = self.get('tags')
        return r.json()

    def create_tags(self, tag=None, color=None):
        """
        Create new inventory tag(s).  Can submit single tag or a list of tags. Can only submit a single color.
        https://api.riskiq.net/api/workspace/#!/default/post_v0_workspace_tag

        :param tag: type str, required
        :param color: type str, required
        """
        ws = Workspace()
        configure_api(ws, context=self.get_context())

        r = ws.create_tags(tag=tag, color=color)
        return r

    def delete_tags(self, tag=None):
        """
        Delete inventory tag(s).  Can submit single tag/tag_id or a list of tags/tag_ids.
        https://api.riskiq.net/api/workspace/#!/default/delete_v0_workspace_tag

        :param tag: type str/list, required
        """
        ws = Workspace()
        configure_api(ws, context=self.get_context())

        r = ws.delete_tags(tag=tag, gi_api=self)
        return r

    def get_brands(self):
        """
        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_brands
        """
        r = self.get('brands')
        return r.json()
    
    def create_brands(self, brand=None):
        """
        Create new inventory brand(s).  Can submit single brand or a list of brands
        https://api.riskiq.net/api/workspace/#!/default/post_v0_workspace_brand

        :param brand: type str/list, required
        """
        ws = Workspace()
        configure_api(ws, context=self.get_context())

        r = ws.create_brands(brand=brand)
        return r

    def delete_brands(self, brand=None):
        """
        Delete brand tag(s).  Can submit single brand/brand_id or a list of brands/brand_ids.
        https://api.riskiq.net/api/workspace/#!/default/delete_v0_workspace_brand

        :param brand: type str/list, optional
        :parag brand_id: type str/list, optional
        """
        ws = Workspace()
        configure_api(ws, context=self.get_context())

        r = ws.delete_brands(brand=brand, gi_api=self)
        return r

    def get_organizations(self):
        """
        # https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_organizations
        """
        r = self.get('organizations')
        return r.json()

    def create_organizations(self, organization=None):
        """
        Create new inventory organization(s).  Can submit single organization or a list of organizations
        https://api.riskiq.net/api/workspace/#!/default/post_v0_workspace_organization

        :param organization: type str/list, required
        """
        ws = Workspace()
        configure_api(ws, context=self.get_context())

        r = ws.create_organizations(organization=organization)
        return r
    
    def delete_organizations(self, organization=None):
        """
        Delete organization tag(s).  Can submit single organization/organization_id or a list of organizations/organization_ids.
        https://api.riskiq.net/api/workspace/#!/default/delete_v0_workspace_organization

        :param organization: type str/list, optional
        :parag organization_id: type str/list, optional
        """

        ws = Workspace()
        configure_api(ws, context=self.get_context())

        r = ws.delete_organizations(organization=organization, gi_api=self)
        return r

    def add_asset(self, asset_name=None, asset_type=None, asset_name_type_list=None, confirm=False, targetAssetTypes=None):
        """
        # https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_assets_add

        :param asset_name: type str (requires asset_type)
        :param asset_type: type str (requires asset_name)
        :param asset_name_type_list: type list - optional ( ex. [{"name":asset_name,"type":asset_type}, ...] )
        :param confirm: type bool (optional - default: False) A boolean value to indicate if the asset state should be CONFIRMED into inventory (confirm: true) or as a CANDIDATE asset in inventory (confirm: false or not specified)
        :param targetAssetTypes: type str or type list - A string or array of target asset types to also add to inventory, along with any supplied properties, that are connected to the asset identifiers (e.g. an asset identifier for a PAGE can cascade the properties to all known IPs for that PAGE).
        """

        _tat = []
        if targetAssetTypes != None:
            if type(targetAssetTypes) == list:
                for a in targetAssetTypes:
                    _t = Value(self)
                    _t.assetType = a
                    _tat.append(_t.assetType)
            else:
                _t = Value(self)
                _t.assetType = targetAssetTypes
                _tat.append(_t.assetType)
        else:
            _t = Value(self)
            _t.assetType = asset_type
            _tat.append(_t.assetType)
        targetAssetTypes = _tat

        this_asset_list = []
        if asset_name_type_list != None:
            _antl = Value(self)
            _antl.assetNameTypeList = asset_name_type_list
            for a in _antl.value:
                _t = Value(self)
                _t.assetType = a['type']
                this_asset_list.append(
                    {'name':a['nmae'],'type':_t.assetType}
                )
        elif asset_name != None:
            _an = Value(self)
            try:
                _an.listType = asset_name
                for a in _an.value:
                    _t = Value(self)
                    _t.assetType = asset_type
                    this_asset_list.append(
                        {'name':a,'type':_t.assetType}
                    )
            except:
                _an.stringType = asset_name
                _t = Value(self)
                _t.assetType = asset_type
                this_asset_list = [
                    {'name':_an.value,'type':_t.assetType}
                ]
        else:
            raise ValueError('GlobalInventory.add_asset() must include asset_name or asset_name_type_list')

        this_payload = {
            'assets' : this_asset_list,
            'properties' : [
                {'name':'removedState','value':'DISMISSED'}
            ],
            'confirm': confirm,
            'targetAssetTypes': targetAssetTypes
        }

        r=self.post('assets/add', payload=this_payload)
        return r.json()

    def remove_asset(self, asset_name=None, asset_type=None, asset_name_type_list=None, targetAssetTypes=None):
        """
        # https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_update

        :param asset_name: type str (requires asset_type)
        :param asset_type: type str (requires asset_name)
        :param asset_name_type_list: type list - optional ( ex. [{"name":asset_name,"type":asset_type}, ...] )
        :param targetAssetTypes: type str or type list - A string or array of target asset types to also add to inventory, along with any supplied properties, that are connected to the asset identifiers (e.g. an asset identifier for a PAGE can cascade the properties to all known IPs for that PAGE).
        """

        _tat = []
        if targetAssetTypes != None:
            if type(targetAssetTypes) == list:
                for a in targetAssetTypes:
                    _t = Value(self)
                    _t.assetType = a
                    _tat.append(_t.assetType)
            else:
                _t = Value(self)
                _t.assetType = targetAssetTypes
                _tat.append(_t.assetType)
        else:
            _t = Value(self)
            _t.assetType = asset_type
            _tat.append(_t.assetType)
        targetAssetTypes = _tat
    

        this_asset_list = []
        if asset_name_type_list != None:
            _antl = Value(self)
            _antl.assetNameTypeList = asset_name_type_list
            for a in _antl.value:
                _t = Value(self)
                _t.assetType = a['type']
                this_asset_list.append(
                    {'name':a['nmae'],'type':_t.assetType}
                )
        elif asset_name != None:
            _an = Value(self)
            try:
                _an.listType = asset_name
                for a in _an.value:
                    _t = Value(self)
                    _t.assetType = asset_type
                    this_asset_list.append(
                        {'name':a,'type':_t.assetType}
                    )
            except:
                _an.stringType = asset_name
                _t = Value(self)
                _t.assetType = asset_type
                this_asset_list = [
                    {'name':_an.value,'type':_t.assetType}
                ]
        else:
            raise ValueError('GlobalInventory.remove_asset() must include asset_name or asset_name_type_list')
        
        this_payload = {
            'assets' : this_asset_list,
            'properties' : [
                {'name':'removedState','value':'DISMISSED'}
            ]
        }
        
        r=self.post('update', payload=this_payload)
        return r.json()

    def update_asset(self, action=None, asset_name=None, asset_type=None, update_type=None, update_value=None, failOnError=False):
        """
        # https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_update
        
        :param action: type str, required (must be add or remove)
        :param asset_name: type str, required
        :param asset_type: type str, required
        :param update_type: type str, required (must be in {0})
        :param update_value: type str, required
        :param failOnError: type bool, optional 
        """
        _a = Value(self)

        _a.action = action

        _aval = Value(self)
        _aval.assetType = asset_type
        _aval.value = asset_name
       
        _uval = Value(self)
        _uval.updateType = update_type
        if _uval.updateType == 'state':
            _uval.state = update_value
        elif _uval.updateType == 'removedState':
            _uval.removedState = update_value
        elif _uval.updateType == 'priority':
            _uval.priority = update_value
        elif _uval.updateType == 'enterprise':
            _uval.enterprise = update_value
        elif _uval.updateType == 'brand':
            _uval.brand = update_value
        elif _uval.updateType == 'organization':
            _uval.organization = update_value
        elif _uval.updateType == 'tag':
            _uval.tag = update_value
        else:
            _uval.value = update_value
        
        this_params = {
            'failOnError':failOnError
        }

        asset_list = []
        if type(_aval.value) == list:
            if len(_aval.value) < 1000:
                for n in _aval.value:
                    this_n = {
                        'name':n,
                        'type':_aval.assetType.upper()
                    }
                    asset_list.append(this_n)
            else:
                bulk_submit_results = bulk_update(self, payload=_aval.value, params=this_params, action=_a.action, asset_type=_aval.assetType, update_type=_uval.updateType, update_value=_uval.value)
                return bulk_submit_results
        else:
            asset_list = [{
                'name':_aval.value,
                'type':_aval.assetType.upper()
            }]

        this_payload = {
            'assets': asset_list,
            'properties': [{
                    'name': _uval.updateType, 
                    'value': _uval.value,
                    'action': _a.action.upper()
                }]}
        r = self.post('update', payload=this_payload, params=this_params)
        return r.json()


def bulk_update(self, payload=None, params=None, action=None, asset_name=None, asset_type=None, update_type=None, update_value=None, failOnError=False):
    count = 0
    bundle_size = 1000
    total_results = []
    bundle_submit = []
    for index in range(len(payload)): 
        count += 1
        if count >= 1000 or index+1 == len(payload):
            count = 0
            this_payload = {
                'assets': bundle_submit,
                'properties': [{
                        'name': update_type, 
                        'value': update_value,
                        'action': action.upper()
                    }]}
            r = self.post('update', payload=this_payload, params=params)
            total_results.append(r.json())
            bundle_submit = []
        else:
            submit_n = {
                'name':payload[index],
                'type':asset_type.upper()
            }
            bundle_submit.append(submit_n)

    return total_results


def get_asset_dataset(self, this_dataset, asset_name=None, asset_type=None, recent=True, size=100):
    _an = Value(self)
    _an.stringType = asset_name
    
    _t = Value(self)
    _t.assetType = asset_type

    this_params = {
        'name':_an.value,
        'global':False,
        'size':size,
        'mark':'*'
    }
    r = self.get('assets/{0}/{1}'.format(_t.assetType.lower(), this_dataset), params=this_params)
    return r


def bundler(endpoint=None, payload=None, asset_type=None, bundle_size=10):
    if endpoint == 'assets/bulk':
        full_payload = []
        host_bundle = []
        count = 0
        for a in payload:
            count +=1
            host_bundle.append({
                "name": a,
                "type": asset_type
            })
            if int(len(host_bundle) % 10) == 0 or a ==payload[-1]:
                full_payload.append(host_bundle)
                host_bundle = []

        return full_payload
    

def bulk_threader(i, _queue, total_size, context, _resultList, _retryList, endpoint):
    while True:
        if not _queue.empty():
            QUEUE_LOCK.acquire()
            _this = _queue.get()
            QUEUE_LOCK.release()

            get_data(_this, context, i, total_size, _resultList, _retryList, endpoint)

            _queue.task_done()

def bulk_sequencer(endpoint=None, payload=None, params=None, asset_type=None, context=None, max_thread_count=25):
    _resultList = []
    _retryList = []
    _queue = queue.Queue()
    if len(payload) < max_thread_count:
        _size = len(payload)
    else:
        _size = max_thread_count
    for i in range(_size):       
        thread = threading.Thread(target=bulk_threader, args=(i, _queue, len(payload), context, _resultList, _retryList, endpoint))
        thread.setDaemon(True)
        thread.start()
    host_bundle = []
    for index in range(len(payload)):
        _queue.put(payload[index])
    _queue.join()
    return {'resultList': _resultList, 'retryList': _retryList}
    
def get_data(data=None, context=None, i=None, qsize=None, _resultList=None, _retryList=None, endpoint=None):
    gi = GlobalInventory()
    configure_api(gi, context=context)
    this_payload = {'assets': data}
    r = gi.post(endpoint, payload=this_payload, thread_data={'threadindex':i,'qsize':qsize})
    if type(r) == dict and 'error' in r.keys():
        for h in r.get('payload').get('assets'):
            _retryList.append(h.get('name'))
    else:
        for h in r.json():
            _resultList.append(h)
