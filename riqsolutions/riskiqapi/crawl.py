from .riskiqapi import RiskIQAPI


class Crawl(RiskIQAPI):
    def __init__(self, api_token=None, api_key=None):
        super().__init__(
            api_token, 
            api_key, 
            url_prefix='v1/page', 
            hostname='ws.riskiq.net')

    def get_crawled(self, start=None, end=None):
        """
        https://sf.riskiq.net/crawlview/api/docs/controllers/PageController.html#crawled
        start: Date Required	(Start date is inclusive)
        end: Date Required (End date is exclusive)
        date format: yyyy-MM-dd
        """
        reqs = ''
        if start == None:
            reqs += ' ** start date required'
        if end == None:
            reqs += ' ** end date required'
        if reqs != '':
            raise ValueError(reqs)

        this_params = {
            'start':start,
            'end': end
        }

        r = self.get('crawled', params=this_params)
        return r.json()

    def get_crawl(self, crawl_guid=None):
        """
        https://sf.riskiq.net/crawlview/api/docs/controllers/PageController.html#crawl
        crawl_guid: required
        """
        reqs = ''
        if crawl_guid == None:
            reqs += ' ** crawl guid required'
        if reqs != '':
            raise ValueError(reqs)

        r = self.get('crawl/{0}'.format(crawl_guid))
        return r.json()

    def get_page(self, crawl_guid=None, page_guid=None):
        """
        https://sf.riskiq.net/crawlview/api/docs/controllers/PageController.html#get
        crawl_guid: required
        page_guid: required
        """
        reqs = ''
        if crawl_guid == None:
            reqs += ' ** crawl guid required'
        if page_guid == None:
            reqs += ' ** page guid required'
        if reqs != '':
            raise ValueError(reqs)

        r = self.get('{0}/{1}'.format(crawl_guid,page_guid, xml=True))
        return r