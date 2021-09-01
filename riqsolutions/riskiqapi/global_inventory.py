from .riskiqapi import RiskIQAPI


class GlobalInventory(RiskIQAPI):
    def __init__(self, api_token=None, api_key=None):
        super().__init__(
            api_token, 
            api_key, 
            url_prefix='/v1/globalinventory', 
            hostname='api.riskiq.net')
    
    def get_tags(self):
        r = self.get('tags')
        return r.json()