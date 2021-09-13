from .riskiqapi import RiskIQAPI
#import os
import logging
# from logging.handlers import RotatingFileHandler
# import inspect
# import re

# m = re.search('\/lib\/python(.*)', os.path.dirname(inspect.getfile(inspect))).group()
# module_path = '{0}{1}/site-packages/riqsolutions/riskiqapi'.format(os.getcwd(), m)

# log_formatter = logging.Formatter('%(asctime)s %(levelname)s - %(module)s:%(funcName)s(): %(message)s')
# logFile = '{0}/log/riqsolutions.log'.format(module_path)
# my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
# my_handler.setFormatter(log_formatter)
# my_handler.setLevel(logging.INFO)
# app_log = logging.getLogger('root')
# logging.setLevel(logging.INFO)
# logging.addHandler(my_handler)

logger = logging.getLogger(__name__)

class LandingPage(RiskIQAPI):
    def __init__(self, api_token=None, api_key=None, proxy=None, context=None):
        super().__init__(
            api_token, 
            api_key, 
            proxy,
            context,
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
            logger.error(reqs)
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