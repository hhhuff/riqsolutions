"""Workspace Module for the RiskIQ Solutions Python API Library"""

from .riskiqapi import RiskIQAPI
from .values import Value

class Workspace(RiskIQAPI):
    """
    Represents a request to the Workspace Management API
    https://api.riskiq.net/api/workspace/

    ** This is an Internal class and not intended to be called by the user **
    """
    def __init__(self, api_token=None, api_key=None, context=None, url_prefix='v0/workspace'):
        super().__init__(
            api_token, 
            api_key, 
            context,
            url_prefix=url_prefix, 
            hostname='api.riskiq.net')
    

    def get_tags(self):
        r = self.get('tag')
        return r.json()

    def create_tags(self, tag=None, color=None):
        """
        Create new inventory tag(s).  Can submit single tag or a list of tags. Can only submit a single color.
        https://api.riskiq.net/api/workspace/#!/default/post_v0_workspace_tag

        :param tag: type str, required
        :param color: type str, required
        """

        _t = Value(self)
        try:
            _t.stringType = tag
        except:
            _t.listType = tag

        _c = Value(self)
        _c.color = color

        this_tags = []
        if type(_t.value) is list:
            for t in _t.value:
                this_t = {
                    'name': t,
                    'color': _c.color,
                    'type': 'INVENTORY'
                }
                this_tags.append(this_t)
        else:
            this_tags = [{
                'name': _t.value,
                'color': _c.color,
                'type': 'INVENTORY'
            }]

        this_payload = {
            'tags': this_tags
        }

        r = self.post('tag', payload=this_payload)
        return r.json()

    def delete_tags(self, tag=None, gi_api=None):
        """
        Delete inventory tag(s).  Can submit single tag/tag_id or a list of tags/tag_ids.
        https://api.riskiq.net/api/workspace/#!/default/delete_v0_workspace_tag

        :param tag: type str/list, optional
        """

        this_tags = []
        _t = Value(gi_api)
        _t.tag = tag
        if type(_t.value) is list:
            for t in _t.value:
                for k,v in t.items():
                    this_t = {
                            'name':k,
                            'id':v
                        }
                    this_tags.append(this_t)
        else:
            for k,v in _t.value.items():
                this_t = {
                    'name':k,
                    'id':v
                }
                this_tags.append(this_t)
            
        this_payload = {
            'tags': this_tags
        }
        r = self.delete('tag', payload=this_payload)
        return r.json()

    def get_brands(self):
        r = self.get('brand')
        return r.json()
    
    def create_brands(self, brand=None):
        """
        Create new inventory brand(s).  Can submit single brand or a list of brands
        https://api.riskiq.net/api/workspace/#!/default/post_v0_workspace_brand

        :param brand: type str/list, required
        """

        _b = Value(self)
        try:
            _b.stringType = brand
        except:
            _b.listType = brand

        this_brands = []
        if type(_b.value) is list:
            for b in _b.value:
                this_b = {
                    'name': b
                }
                this_brands.append(this_b)
        else:
            this_brands = [{
                'name': _b.value
            }]

        this_payload = {
            'brands': this_brands
        }

        r = self.post('brand', payload=this_payload)
        return r.json()

    def delete_brands(self, brand=None, gi_api=None):
        """
        Delete inventory brand(s).  Can submit single brand/brand_id or a list of brands/brand_ids.
        https://api.riskiq.net/api/workspace/#!/default/delete_v0_workspace_brand

        :param brand: type str/list, optional
        """

        this_brands = []
        _b = Value(gi_api)
        _b.brand = brand
        if type(_b.value) is list:
            for b in _b.value:
                for k,v in b.items():
                    this_b = {
                            'name':k,
                            'id':v
                        }
                    this_brands.append(this_b)
        else:
            for k,v in _b.value.items():
                this_b = {
                    'name':k,
                    'id':v
                }
                this_brands.append(this_b)
            
        this_payload = {
            'brands': this_brands
        }
        r = self.delete('brand', payload=this_payload)
        return r.json()

    def get_organizations(self):
        r = self.get('organization')
        return r.json()

    def create_organizations(self, organization=None):
        """
        Create new inventory organization(s).  Can submit single organization or a list of organizations
        https://api.riskiq.net/api/workspace/#!/default/post_v0_workspace_organization

        :param organization: type str/list, required
        """

        _o = Value(self)
        try:
            _o.stringType = organization
        except:
            _o.listType = organization

        this_organizations = []
        if type(_o.value) is list:
            for o in _o.value:
                this_o = {
                    'name': b
                }
                this_organizations.append(this_o)
        else:
            this_organizations = [{
                'name': _o.value
            }]

        this_payload = {
            'organizations': this_organizations
        }

        r = self.post('organization', payload=this_payload)
        return r.json()

    def delete_organizations(self, organization=None, gi_api=None):
        """
        Delete inventory organization(s).  Can submit single organization/organization_id or a list of organizations/organization_ids.
        https://api.riskiq.net/api/workspace/#!/default/delete_v0_workspace_organization

        :param organization: type str/list, optional
        """

        this_organizations = []
        _o = Value(gi_api)
        _o.organization = organization
        if type(_o.value) is list:
            for o in _o.value:
                for k,v in o.items():
                    this_o = {
                            'name':k,
                            'id':v
                        }
                    this_organizations.append(this_o)
        else:
            for k,v in _o.value.items():
                this_o = {
                    'name':k,
                    'id':v
                }
                this_organizations.append(this_o)
            
        this_payload = {
            'organizations': this_organizations
        }
        r = self.delete('organization', payload=this_payload)
        return r.json()
