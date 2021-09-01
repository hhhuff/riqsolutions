from .riskiqapi import RiskIQAPI


class LandingPage(RiskIQAPI):
    def __init__(self, api_token=None, api_key=None):
        super().__init__(
            api_token, 
            api_key, 
            url_prefix='v1/landingPage', 
            hostname='ws.riskiq.net')

    def get_landingPageProjects(self, **kwargs):
        r = self.get('projects')
        return r.json()

    def get_landingPage(self, **kwargs):
        """
        # https://sf.riskiq.net/crawlview/api/docs/controllers/LandingPageController.html#get
        # md5 or version_id: required
        # causeTree: optional (default: True)
        """
        reqs = ''
        if kwargs.get('md5') == None and kwargs.get('version_id') == None:
            reqs += ' ** md5 or version_id required'
        if kwargs.get('md5') != None and kwargs.get('version_id') != None:
            reqs += ' ** Only one of md5 or version_id is allowed'
        if reqs != '':
            raise ValueError(reqs)

        if kwargs.get('md5') != None:
            this_get = kwargs.get('md5') 
        if kwargs.get('version_id') != None:
            this_get = kwargs.get('version_id') 
        if kwargs.get('causeTree') == None:
            kwargs['causeTree'] = True

        this_params = {
            'causeTree':kwargs.get('causeTree')
        }

        r = self.get('assets/{}/connected'.format(this_get), params=this_params)
        return r.json()