from .riskiqapi import RiskIQAPI


class Workspace(RiskIQAPI):
    def __init__(self, api_token=None, api_key=None):
        super().__init__(
            api_token, 
            api_key, 
            url_prefix='v0/workspace', 
            hostname='api.riskiq.net')
    

    def get_tags(self, **kwargs):
        r = self.get('tag')
        return r.json()

    def create_tags(self, tag=None, color=None, **kwargs):
        """
        https://api.riskiq.net/api/workspace/#!/default/post_v0_workspace_tag
        Will only create Inventory Tags
        tag: type(str) or type(list) - required 
        color: type(str) - required
        """
        colors = ['yellow', 'green', 'orange', 'red', 'purple', 'green-2', 'dark-gray', 'blue', 'black', 'white', 'indigo', 'gray']

        reqs = ''
        if tag == None:
            reqs += ' ** tag type(str) or type(list) required'
        if type(tag) != str and type(tag) != list:
            reqs += ' ** tag must be type(str) or type(list)'
        if color == None:
            reqs += ' ** must include color=[yellow, green, orange, red, purple, green-2, dark-gray, blue, black, white, indigo, gray]' 
        if color is not None and color not in colors:
            reqs += ' ** color must be one of: [yellow, green, orange, red, purple, green-2, dark-gray, blue, black, white, indigo, gray]' 
        if reqs != '':
            raise ValueError(reqs)

        this_tags = []
        if type(tag) == list:
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


    def get_brands(self, **kwargs):
        r = self.get('brand')
        return r.json()
    
    def create_brands(self, brand=None, **kwargs):
        """
        https://api.riskiq.net/api/workspace/#!/default/post_v0_workspace_brand
        brand: type(str) or type(list) - required
        """
        reqs = ''
        if brand == None:
            reqs += ' ** brand type(str) or type(list) required'
        if type(brand) != str and type(brand) != list:
            reqs += ' ** brand must be type(str) or type(list)'
        if reqs != '':
            raise ValueError(reqs)

        this_brands = []
        if brand is not None and type(brand) == list:
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


    def get_organizations(self, **kwargs):
        r = self.get('organization')
        return r.json()

    def create_organizations(self, organization=None, *kwargs):
        """
        https://api.riskiq.net/api/workspace/#!/default/post_v0_workspace_organization
        organization: type(str) or type(list) - required 
        """
        reqs = ''
        if organization == None:
            reqs += ' ** organization type(str) or type(list) required'
        if type(organization) != str and type(organization) != list:
            reqs += ' ** organization must be type(str) or type(list)'
        if reqs != '':
            raise ValueError(reqs)

        this_organizations = []
        if type(organization) == list:
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


