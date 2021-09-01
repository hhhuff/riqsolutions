from .riskiqapi import RiskIQAPI


class Events(RiskIQAPI):
    def __init__(self, api_token=None, api_key=None):
        super().__init__(
            api_token, 
            api_key, 
            url_prefix='v1/event', 
            hostname='ws.riskiq.net')

    def get_searchFields(self, **kwargs):
        r = self.get('search/filters')
        return r.json()

    def get_savedSearches(self, **kwargs):
        r = self.get('savedsearches')
        return r.json()
    
    def get_event(self, **kwargs):
        """
        # https://sf.riskiq.net/crawlview/api/docs/controllers/LandingPageController.html#get
        # eventId: required
        # snapshot: optional (default: False) return a snapshot url of the event if set to true
        # classifier: optional (default: False) classifier matches shown in the response
        # includeUserNotes: optional (default: False) notes created by a user added to the response
        """
        reqs = ''
        if kwargs.get('eventId') == None:
            reqs += ' ** eventId required'
        if reqs != '':
            raise ValueError(reqs)

        if kwargs.get('snapshot') != None:
            this_get = False
        if kwargs.get('classifier') != None:
            this_get = False
        if kwargs.get('includeUserNotes') != None:
            kwargs['includeUserNotes'] = False

        this_params = {
            'snapshot':kwargs.get('snapshot'),
            'classifier':kwargs.get('classifier'),
            'includeUserNotes':kwargs.get('includeUserNotes')
        }

        r = self.get(eventId, params=this_params)
        return r.json()