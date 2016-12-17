import copy
import time
import hashlib
import requests

KEY = 'AKIAIOSFODNN7EXAMPLE'
SECRET = '1234567890'
URL = 'http://webservices.amazon.com/onca/xml?'
PARAMS = {
    'Service': 'AWSECommerceServic',
    'AWSAccessKeyId': '',
    'Operation': 'ItemLookup',
    'ItemId': '',
    'ResponseGroup': 'ItemAttributes,Reviews',
    'Version': '2013-08-01',
    'Timestamp': '',
}


def item_search():
    pass


def item_lookup(item_id):
    params = copy.copy(PARAMS)
    params['ItemId'] = item_id
    params['Timestamp'] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime(None))
    param_list = ['{key}={value}' for key, value in params.items()]
    param_list.sort()
    param_str = '&'.join(params)
    sig_str = '\n'.join(['GET', 'webservices.amazon.com', '/onca/xml', param_str])
    m = hashlib.md5()
    sig_str.encode('utf-8')
    data = requests.get(URL+param_str)
    print(data)
