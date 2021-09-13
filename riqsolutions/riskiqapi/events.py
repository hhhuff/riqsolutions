from .riskiqapi import RiskIQAPI

class Events(RiskIQAPI):
    def __init__(self, api_token=None, api_key=None, proxy=None, context=None):
        super().__init__(
            api_token, 
            api_key, 
            proxy,
            context,
            url_prefix='v1/event', 
            hostname='ws.riskiq.net')

    def get_searchFields(self):
        r = self.get('search/filters')
        return r.json()

    def get_savedSearches(self):
        r = self.get('savedsearches')
        return r.json()
    
    def get_event(self, eventId=None, snapshot=None, classifier=None, includeUserNotes=None):
        """
        # https://sf.riskiq.net/crawlview/api/docs/controllers/LandingPageController.html#get
        # eventId: required
        # snapshot: optional (default: False) return a snapshot url of the event if set to true
        # classifier: optional (default: False) classifier matches shown in the response
        # includeUserNotes: optional (default: False) notes created by a user added to the response
        """
        reqs = ''
        if eventId is None:
            reqs += ' ** eventId required'
        if reqs != '':
            raise ValueError(reqs)

        this_params = {
            'snapshot':snapshot,
            'classifier':classifier,
            'includeUserNotes':includeUserNotes
        }

        r = self.get(eventId, params=this_params)
        return r.json()