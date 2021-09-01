from .riskiqapi import RiskIQAPI


class Crawl(RiskIQAPI):
    def __init__(self, api_token=None, api_key=None):
        super().__init__(
            api_token, 
            api_key, 
            url_prefix='v1/page', 
            hostname='ws.riskiq.net')

    def get_crawled(self, **kwargs):
        """
        https://sf.riskiq.net/crawlview/api/docs/controllers/PageController.html#crawled
        start: Date Required	(Start date is inclusive)
        end: Date Required (End date is exclusive)
        date format: yyyy-MM-dd
        """
        reqs = ''
        if kwargs.get('start') == None:
            reqs += ' ** start date required'
        if kwargs.get('end') == None:
            reqs += ' ** end date required'
        if reqs != '':
            raise ValueError(reqs)

        this_params = {
            'start':kwargs.get('start'),
            'end': kwargs.get('end')
        }

        r = self.get('crawled', params=this_params)
        return r.json()

    def get_crawl(self, **kwargs):
        """
        https://sf.riskiq.net/crawlview/api/docs/controllers/PageController.html#crawl
        crawl_guid: required
        """
        reqs = ''
        if kwargs.get('crawl_guid') == None:
            reqs += ' ** crawl guid required'
        if reqs != '':
            raise ValueError(reqs)

        r = self.get('crawl/{0}'.format(kwargs.get('crawl_guid')))
        return r.json()

    def get_page(self, **kwargs):
        """
        https://sf.riskiq.net/crawlview/api/docs/controllers/PageController.html#get
        crawl_guid: required
        page_guid: required
        """
        reqs = ''
        if kwargs.get('crawl_guid') == None:
            reqs += ' ** crawl guid required'
        if kwargs.get('page_guid') == None:
            reqs += ' ** page guid required'
        if reqs != '':
            raise ValueError(reqs)

        r = self.get('{0}/{1}'.format(kwargs.get('crawl_guid'),kwargs.get('page_guid')), xml=True)
        return r