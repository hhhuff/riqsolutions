from .riskiqapi import RiskIQAPI


class Workspace(RiskIQAPI):
    def __init__(self, api_token=None, api_key=None):
        super().__init__(
            api_token, 
            api_key, 
            url_prefix='v0/workspace', 
            hostname='api.riskiq.net')
    

    def get_tags(self):
        r = self.get('tag')
        return r.json()

    def create_tags(self, tag=None, color=None):
        """
        https://api.riskiq.net/api/workspace/#!/default/post_v0_workspace_tag
        Will only create Inventory Tags
        tag: type(str) or type(list) - required 
        color: type(str) - required
        """
        colors = ['yellow', 'green', 'orange', 'red', 'purple', 'green-2', 'dark-gray', 'blue', 'black', 'white', 'indigo', 'gray']

        reqs = ''
        if tag is None:
            reqs += ' ** tag type(str) or type(list) required'
        if type(tag) != str and type(tag) != list:
            reqs += ' ** tag must be type(str) or type(list)'
        if color is None:
            reqs += ' ** must include color=[yellow, green, orange, red, purple, green-2, dark-gray, blue, black, white, indigo, gray]' 
        if color is not None and color not in colors:
            reqs += ' ** color must be one of: [yellow, green, orange, red, purple, green-2, dark-gray, blue, black, white, indigo, gray]' 
        if reqs != '':
            raise ValueError(reqs)

        this_tags = []
        if type(tag) is list:
            for t in tag:
                this_o = {
                    'name': t,
                    'color': color,
                    'type': 'INVENTORY'
                }
                this_tags.append(this_t)
        else:
            this_tags = [{
                'name': tag,
                'color': color,
                'type': 'INVENTORY'
            }]

        this_payload = {
            'tags': this_tags
        }

        r = self.post('tag', payload=this_payload)
        return r.json()

    def delete_tags(self, tag_id=None):
        """
        https://api.riskiq.net/api/workspace/#!/default/delete_v0_workspace_tag
        tag_id: type(dict) or type(list of dicts) - required - format {tag_id type(int):tag_name type(str)}
            example: {123456:'example_tag'} or [{123456:'example_tag'},{654321:'example_tag_2'}]
        """

        reqs = ''
        if tag_id is None:
            reqs += ' ** tag_id: type(dict) or type(list of dicts) - required - format {tag_id type(int):tag_name type(str)}'
        if tag_id is not None and type(tag_id) is not dict and type(tag_id) is not list:
            reqs += ' ** tag_id must be type(dict) or type(list)'
        if reqs != '':
            raise ValueError(reqs)

        this_tags = []
        if type(tag_id) is list:
            for index in range(len(tag_id)):
                this_t = {
                    'id': list(tag_id[index].keys())[0],
                    'name': list(tag_id[index].values())[0]
                }
                this_tags.append(this_t)
        else:
            this_t = {
                'id': list(tag_id.keys())[0],
                'name': list(tag_id.values())[0]
            }
            this_tags.append(this_t)

        this_payload = {
            'tags': this_tags
        }

        r = self.delete('tag', payload=this_payload)
        return r.status_code

    def get_brands(self):
        r = self.get('brand')
        return r.json()
    
    def create_brands(self, brand=None):
        """
        https://api.riskiq.net/api/workspace/#!/default/post_v0_workspace_brand
        brand: type(str) or type(list) - required
        """
        reqs = ''
        if brand is None:
            reqs += ' ** brand type(str) or type(list) required'
        if type(brand) != str and type(brand) != list:
            reqs += ' ** brand must be type(str) or type(list)'
        if reqs != '':
            raise ValueError(reqs)

        this_brands = []
        if brand is not None and type(brand) is list:
            for b in brand:
                this_b = {
                    'name': b
                }
                this_brands.append(this_b)
        else:
            this_brands = [{'name':brand}]

        this_payload = {
            'brands': this_brands
        }
        r = self.post('brand', payload=this_payload)
        return r.json()

    def delete_brands(self, brand_id=None):
        """
        https://api.riskiq.net/api/workspace/#!/default/delete_v0_workspace_tag
        brand_id: type(dict) or type(list of dicts) - required - format {brand_id type(int):brand_name type(str)}
            example: {123456:'example_brand'} or [{123456:'example_brand'},{654321:'example_brand_2'}]

        """
        reqs = ''
        if brand_id is None:
            reqs += ' ** brand_id: type(dict) or type(list of dicts) - required - format {brand_id type(int):brand_name type(str)}'
        if brand_id is not None and type(brand_id) is not dict and type(brand_id) is not list:
            reqs += ' ** brand_id must be type(dict) or type(list)'
        if reqs != '':
            raise ValueError(reqs)

        this_brands = []
        if type(brand_id) is list:
            for index in range(len(brand_id)):
                this_b = {
                    'id': list(brand_id[index].keys())[0],
                    'name': list(brand_id[index].values())[0]
                }
                this_brands.append(this_b)
        else:
            this_b = {
                'id': list(brand_id.keys())[0],
                'name': list(brand_id.values())[0]
            }
            this_brands.append(this_b)

        this_payload = {
            'brands': this_brands
        }

        r = self.delete('brand', payload=this_payload)
        return r.status_code

    def get_organizations(self):
        r = self.get('organization')
        return r.json()

    def create_organizations(self, organization=None):
        """
        https://api.riskiq.net/api/workspace/#!/default/post_v0_workspace_organization
        organization: type(str) or type(list) - required 
        """
        reqs = ''
        if organization is None:
            reqs += ' ** organization type(str) or type(list) required'
        if type(organization) != str and type(organization) != list:
            reqs += ' ** organization must be type(str) or type(list)'
        if reqs != '':
            raise ValueError(reqs)

        this_organizations = []
        if type(organization) is list:
            for o in organization:
                this_o = {
                    'name': o
                }
                this_organizations.append(this_o)
        else:
            this_organizations = [{'name':organization}]

        this_payload = {
            'organizations': this_organizations
        }
        r = self.post('organization', payload=this_payload)
        return r.json()

    def delete_organizations(self, org_id=None):
        """
        https://api.riskiq.net/api/workspace/#!/default/delete_v0_workspace_tag
        org_id: type(dict) or type(list of dicts) - required - format {org_id type(int):org_name type(str)}
            example: {123456:'example_org'} or [{123456:'example_org'},{654321:'example_org_2'}]

        """
        reqs = ''
        if org_id is None:
            reqs += ' ** org_id: type(dict) or type(list of dicts) - required - format {org_id type(int):org_name type(str)}'
        if org_id is not None and type(org_id) is not dict and type(org_id) is not list:
            reqs += ' ** org_id must be type(dict) or type(list)'
        if reqs != '':
            raise ValueError(reqs)

        this_orgs = []
        if type(org_id) is list:
            for index in range(len(org_id)):
                this_b = {
                    'id': list(org_id[index].keys())[0],
                    'name': list(org_id[index].values())[0]
                }
                this_orgs.append(this_b)
        else:
            this_b = {
                'id': list(org_id.keys())[0],
                'name': list(org_id.values())[0]
            }
            this_orgs.append(this_b)

        this_payload = {
            'organizations': this_orgs
        }

        r = self.delete('organization', payload=this_payload)
        return r.status_code
