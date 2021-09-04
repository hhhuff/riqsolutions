from .riskiqapi import RiskIQAPI


class LandingPage(RiskIQAPI):
    def __init__(self, api_token=None, api_key=None):
        super().__init__(
            api_token, 
            api_key, 
            url_prefix='v1/landingPage', 
            hostname='ws.riskiq.net')

    def get_landingPageProjects(self):
        r = self.get('projects')
        return r.json()

    def get_landingPage(self, md5=None, version_id=None, causeTree=True):
        """
        # https://sf.riskiq.net/crawlview/api/docs/controllers/LandingPageController.html#get
        # md5 or version_id: required
        # causeTree: optional (default: True)
        """
        reqs = ''
        if md5 == None and version_id == None:
            reqs += ' ** md5 or version_id required'
        if md5 != None and version_id != None:
            reqs += ' ** Only one of md5 or version_id is allowed'
        if reqs != '':
            raise ValueError(reqs)
        
        if md5 is not None:
            this_get = md5
        if version_id is not None:
            this_get = version_id

        this_params = {
            'causeTree':causeTree
        }

        r = self.get(this_get, params=this_params)
        return r.json()