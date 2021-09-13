"""Global Inventory Module for the RiskIQ Solutions Python API Library"""

from .riskiqapi import RiskIQAPI
import json

ASSET_TYPES = ['DOMAIN', 'HOST', 'PAGE', 'IP_BLOCK', 'IP_ADDRESS', 'CONTACT', 'SSL_CERT', 'AS']

class GlobalInventory(RiskIQAPI):
    """
    Represents a Global Inventory Asset (or list of Assets)
    """
    def __init__(self, api_token=None, api_key=None, proxy=None, context=None):
        super().__init__(
            api_token, 
            api_key, 
            proxy,
            context,
            url_prefix='v1/globalinventory', 
            hostname='api.riskiq.net')
    

    def inventory_search(self, query: json=None, size: int=100, page: int=0):
        """
        Submit json which was generated from the UI to retrieve results through the API. 
        https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_search
        :param query: type json
        :param global: type bool, optional
        :param size: type int), optional
        :param page: type int), optional

        :returns: {'results':r}
        """
        reqs = ''
        if query == None:
            reqs += ' ** a query type dict) is required'
        if reqs != '':
            raise ValueError(reqs)

        this_params = {
            'global':False,
            'size':size,
            'mark':'*'
        }
        r = self.post('search', payload=query, params=this_params)
        return {'results':r}

    def get_asset_by_id(self, uuid: str=None, recent: bool=True):
        """
        Submit the UUID of an asset to retrieve its record
        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_assets_id_uuid
        :param uuid: type str
        :param recent: type bool, optional
        :param global: type bool, optional
        """
        # reqs = ''
        # if uuid == None:
        #     reqs += ' ** uuid type str required'
        # if reqs != '':
        #     raise ValueError(reqs)

        this_params = {
            'recent':recent,
            'global':False
        }

        r = self.get('assets/id/{}'.format(uuid), params=this_params)
        return r.json()

    def get_asset(self, asset_name=None, asset_type=None, recent=True, size=100):
        """
        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_assets_type
        :param asset_type: type str
        :param asset_name: type str
        :param recent: type bool, optional
        :param global: type bool, optional 
        :param size: type int, optional
        """
        reqs = ''
        if asset_type == None:
            reqs += ' ** asset_type type str required'
        if asset_name == None:
            reqs += ' ** asset_name type str'
        if reqs != '':
            raise ValueError(reqs)

        this_params = {
            'name':asset_name,
            'recent':recent,
            'global':False,
            'size':size
        }

        r = self.get('assets/{}'.format(asset_type), params=this_params)
        return r.json()

    def get_assets_bulk(self, asset_list:None, asset_type=None):
        """
        https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_assets_bulk
        :param asset_type: type str
        :param asset_list: type list
        """
        reqs = ''
        if asset_type == None:
            reqs += ' ** asset_type type str required'
        if asset_list == None:
            reqs += ' ** asset_list type list'
        if asset_list is not None and type(asset_list) is not list:
            reqs += ' ** asset_list must be type list'
        if reqs != '':
            raise ValueError(reqs)

        if len(asset_list) < 100:
            assets = []
            for a in asset_list:
                this_asset = {
                    "name": a,
                    "type": asset_type
                }
                assets.append(this_asset)
            
            this_payload = {
                'assets':assets
            }
        else:
            r = bulk_get(self, payload=asset_list, asset_type=asset_type)
            return r

        r = self.post('assets/bulk', payload=this_payload)
        return r.json()

    def get_asset_attributes(self, asset_name=None, asset_type=None, recent=True, size=100, page=0):
        r = get_asset_dataset(self, 'attributes', asset_name, asset_type, recent, size, page)
        return {'results':r}

    def get_asset_cookies(self, asset_name=None, asset_type=None, recent=True, size=100, page=0):
        r = get_asset_dataset(self, 'cookies', asset_name, asset_type, recent, size, page)
        return {'results':r}

    def get_asset_hostpairs(self, asset_name=None, asset_type=None, recent=True, size=100, page=0):
        r = get_asset_dataset(self, 'hostPairs', asset_name, asset_type, recent, size, page)
        return {'results':r}

    def get_asset_minicrawls(self, asset_name=None, asset_type=None, recent=True, size=100, page=0):
        r = get_asset_dataset(self, 'miniCrawls', asset_name, asset_type, recent, size, page)
        return {'results':r}

    def get_asset_certificates(self, asset_name=None, asset_type=None, recent=True, size=100, page=0):
        r = get_asset_dataset(self, 'sslCerts', asset_name, asset_type, recent, size, page)
        return {'results':r}

    def get_asset_web_components(self, asset_name=None, asset_type=None, recent=True, size=100, page=0):
        r = get_asset_dataset(self, 'webComponents', asset_name, asset_type, recent, size, page)
        return {'results':r}

    def get_asset_connected(self, asset_name=None, asset_type=None, recent=True, size=100, page=0):
        r = get_asset_dataset(self, 'connected', asset_name, asset_type, recent, size, page)
        return {'results':r}
    

    def get_asset_deltas(self, asset_type=None, date=None, delta_range=1, measure='ADDED', brand=None, organization=None, tag=None, size=100, page=0):
        """     
        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_deltas
        :param asset_type: type str
        :param date: type str
        :param delta_range: type int, optional
        :param measure: type str
        :param brand: type str, optional
        :param organization: type str, optional
        :param tag: type str, optional
        :param size: type int, optional
        :param page: type int, optional
        """

        reqs = ''
        if asset_type == None:
            reqs += ' ** asset_type type str required'
        if date == None:
            reqs += ' ** date type str required (YYYY-MM-DD)'
        if measure == None:
            reqs += ' ** measure type str required, must be ADDED or REMOVED'
        if delta_range != None and type(delta_range) != int:
            reqs += ' ** delta_range must be type int) '
        if delta_range != None and delta_range not in [1,7,10]:
            reqs += ' ** delta_range must be 1, 7, or 10'
        if reqs != '':
            raise ValueError(reqs)

        this_params = {
            'type':asset_type,
            'date':date,
            'range': delta_range,
            'measure': measure,
            'brand': brand,
            'organization': organization,
            'tag': tag,
            'size':size,
            'mark':'*'
        }

        r = self.get('deltas',params=this_params)
        return {'results':r}


    def get_asset_deltas_summary(self, date=None, delta_range=1, brand=None, organization=None, tag=None, size=100, page=0):
        """     
        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_deltas_summary
        :param date: type str
        :param delta_range:  type int, optional
        :param brand: type str, optional
        :param organization: type str, optional
        :param tag: type str, optional
        """

        reqs = ''
        if date == None:
            reqs += ' ** date type str required (YYYY-MM-DD)'
        if delta_range != None and type(delta_range) != int:
            reqs += ' ** delta_range must be type int) '
        if delta_range != None and delta_range not in [1,7,10]:
            reqs += ' ** delta_range must be 1, 7, or 10'
        if reqs != '':
            raise ValueError(reqs)

        this_params = {
            'date':date,
            'range': delta_range,
            'brand': brand,
            'organization': organization,
            'tag': tag
        }

        r = self.get('deltas/summary',params=this_params)
        return r.json()


    def get_tasks(self):
        """
        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_tasks
        """
        r = self.get('tasks')
        return r.json()

    def get_task(self, taskid=None):
        """
        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_tasks
        """
        reqs = ''
        if taskid == None:
            reqs += '  ** taskid required'
        if reqs != '':
            raise ValueError(reqs)
        this_params={'id':taskid}
        r = self.get('tasks',params=this_params)
        return r.json()
        

    def get_tags(self):
        """
        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_tags
        """
        r = self.get('tags')
        return r.json()

    def get_brands(self):
        """
        https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_brands
        """
        r = self.get('brands')
        return r.json()

    def get_organizations(self):
        """
        # https://api.riskiq.net/api/globalinventory/#!/default/get_v1_globalinventory_organizations
        """
        r = self.get('organizations')
        return r.json()


    def add_asset(self, asset_name=None, asset_type=None):
        """
        # https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_assets_add
        :param asset_name: type str
        :param asset_type: type str
        """
        reqs = ''
        if asset_type == None:
            reqs += ' ** asset_type required [Host, IPAddress, Page, or Domain]'
        if asset_type != None and asset_type not in ASSET_TYPES:
            reqs += ' ** asset_type must be one of [Host, IPAddress, Page, or Domain]'
        if asset_name == None:
            reqs += ' ** asset_name required (Can be type str or type list))'
        if asset_type is not None and type(asset_name) != str and type(asset_name) != list:
            reqs += ' ** asset_name must be be type str or type list'

        asset_list = []
        if type(asset_name) == list:
            for n in asset_name:
                this_n = {
                    'name':n,
                    'type':asset_type.upper()
                }
                asset_list.append(this_n)
        else:
            asset_list = [{
                'name':asset_name,
                'type':asset_type.upper()
            }]

        this_payload = {
            'assets':asset_list,
                'properties': [
                {
                    'name': 'prioity',
                    'value': 'HIGH'
                }
            ]}
        r=self.post('assets/add', payload=this_payload)
        return r.json()


    def update_asset(self, action=None, asset_name=None, asset_type=None, update_type=None, update_value=None, failOnError=False):
        """
        # https://api.riskiq.net/api/globalinventory/#!/default/post_v1_globalinventory_update
        :param asset_name: type str
        :param asset_type: type str
        :param update_type: type str
        :param update_value: type str
        :param failOnError: type bool, optional 
        """
        reqs = ''
        if action == None:
            reqs += '  ** action required (must be add or remove)'
        if action is not None and action not in ['add','remove']:
            reqs += '  ** action must be add or remove'
        if asset_type == None:
            reqs += ' ** asset_type required'
        if asset_name == None:
            reqs += ' ** asset_name required (Can be type str or type list))'
        if asset_type is not None and type(asset_name) != str and type(asset_name) != list:
            reqs += ' ** asset_name must be be type str or type list'
        if update_type == None:
            reqs += ' ** update_type required (tag, brand, or organization)'
        if update_type is not None and update_type not in ['tag','brand','organization']:
            reqs += ' ** update_type must be tag, brand, or organization)'
        if update_value == None:
            reqs += ' ** update_value required'
        if reqs != '':
            raise ValueError(reqs)

        this_params = {
            'failOnError':failOnError
        }

        asset_list = []
        if type(asset_name) == list:
            if len(asset_name) < 1000:
                for n in asset_name:
                    this_n = {
                        'name':n,
                        'type':asset_type.upper()
                    }
                    asset_list.append(this_n)
            else:
                bulk_submit_results = bulk_update(self, payload=asset_name, params=this_params,action=action, asset_type=asset_type, update_type=update_type, update_value=update_value)
                return bulk_submit_results
        else:
            asset_list = [{
                'name':asset_name,
                'type':asset_type.upper()
            }]

        this_payload = {
            'assets': asset_list,
            'properties': [{
                    'name': update_type, 
                    'value': update_value,
                    'action': action.upper()
                }]}
        r = self.post('update', payload=this_payload, params=this_params)
        return r.json()

def bulk_get(self, payload=None, params=None, asset_type=None):
    count = 0
    bundle_size = 100
    total_results = []
    bundle_submit = []
    for index in range(len(payload)): 
        count += 1
        if count >= bundle_size or index+1 == len(payload):
            count = 0
            this_payload = {
                'assets': bundle_submit
                }
            r = self.post('assets/bulk', payload=this_payload, params=params)
            total_results.append(r.json())
            del bundle_submit[:]
        else:
            submit_n = {
                'name':payload[index],
                'type':asset_type.upper()
            }
            bundle_submit.append(submit_n)

    return total_results


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
            del bundle_submit[:]
        else:
            submit_n = {
                'name':payload[index],
                'type':asset_type.upper()
            }
            bundle_submit.append(submit_n)

    return total_results



def get_asset_dataset(self, this_dataset, asset_name=None, asset_type=None, recent=True, size=100, page=0):
        # """     
        # https://api.riskiq.net/api/globalinventory/
        # asset_type: type str
        # asset_name: type str
        # global: optional (default: False)
        # size: optional (default: 100)
        # page: optional (default: 0)
        # """

        reqs = ''
        if asset_type == None:
            reqs += ' ** asset_type type str required'
        if asset_name == None:
            reqs += ' ** asset_namee type str required'
        if reqs != '':
            raise ValueError(reqs)

        this_params = {
            'name':asset_name,
            'global':False,
            'size':size,
            'mark':'*'
        }
        r = self.get('assets/{0}/{1}'.format(asset_type, this_dataset), params=this_params)
        return r
