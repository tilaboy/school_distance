from urllib import parse
import requests
import re

class BuiduMapClient(object):
    def __init__(self, ak=None, domain='http://api.map.baidu.com'):
        if not ak:
            raise ValueError("Error: a valid ak is required")

        self.ak = ak
        self.domain = domain
        self.output = 'json'

    def get(self, action='place', sub_action='search', params=None):
        request_url = self.generate_url(action, sub_action, params)
        response = requests.get(request_url).json()

        status = response['status']
        if status != 0:
            print ("ERROR:{}".format(status))
            print("ERROR:{}".format(response))
            response = None
            #raise exceptions.StatusError(action, sub_action, status)
        #else:    
            #print("{}/{} suceed on {}".format(action, sub_action, request_url))
        return response

    def generate_url(self, action='place', sub_action='search', params=None):
        # http://api.map.baidu.com/direction/v2/search?

        base_url = '/'.join([self.domain,
                            action,
                            'v2',
                            sub_action]
                            ) + '?'
        addi_url_hash = params.copy()

        addi_url_hash['ak'] = self.ak
        addi_url_hash['output'] = self.output
        addi_url=parse.urlencode(addi_url_hash)
        url = base_url + addi_url
        #print ("url: {}".format(url))
        return url
