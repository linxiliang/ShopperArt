"""API for Amazon."""
import copy
import hmac
import time
import base64
import hashlib
import urllib
import requests
import untangle

KEY = 'AKIAJIU4THDG4KYCA3KQ'
SECRET = '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'
URL = 'http://webservices.amazon.com/onca/xml?'
PARAMS = {
    'Service': 'AWSECommerceServic',
    'AWSAccessKeyId': KEY,
    'AssociateTag': 'isaac07b-20',
    'Operation': 'ItemSearch',
    # 'Operation': 'ItemLookup',
    # 'ItemId': 'B00VQR7MVQ',
    'SearchIndex': 'All',
    # 'ResponseGroup': 'ItemAttributes,Reviews',
    'Timestamp': '',
    # 'Sort': 'psrank',
}
CATS = ['Electronics', 'PCHardware', 'Wireless']


def item_search(keywords):
    """Search Item."""
    params = copy.copy(PARAMS)
    # params['Title'] = keywords
    params['Keywords'] = keywords
    params['Timestamp'] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime(None))
    param_list = ['{key}={value}'.format(
        key=key, value=urllib.request.quote(value))
        for key, value in params.items()]
    param_list.sort()
    param_str = '&'.join(param_list)
    sig_str = '\n'.join(
        ['GET', 'webservices.amazon.com', '/onca/xml', param_str])
    sig = base64.b64encode(hmac.new(
        SECRET.encode('utf-8'), sig_str.encode('utf-8'),
        hashlib.sha256).digest()).decode('utf-8')
    param_list.append('Signature=' + urllib.request.quote(sig))
    param_str = '&'.join(param_list)
    data = requests.get(URL + param_str)
    print(data.text)
    return data


def item_lookup(item_id):
    """Lookup Item."""
    params = copy.copy(PARAMS)
    params['ItemId'] = item_id
    params['Timestamp'] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime(None))
    param_list = ['{key}={value}'.format(
        key=key, value=urllib.request.quote(value))
        for key, value in params.items()]
    param_list.sort()
    param_str = '&'.join(param_list)
    sig_str = '\n'.join(
        ['GET', 'webservices.amazon.com', '/onca/xml', param_str])
    sig = base64.b64encode(hmac.new(
        SECRET.encode('utf-8'), sig_str.encode('utf-8'),
        hashlib.sha256).digest()).decode('utf-8')
    param_list.append('Signature=' + urllib.request.quote(sig))
    param_str = '&'.join(param_list)
    data = requests.get(URL + param_str)
    print(data.text)
    return data


def parse_data(data):
    """Parse xml data."""
    root = untangle.parse(data.text)
    # print('===>', root.ItemSearchResponse.Items.Item)
    # item = root.ItemSearchResponse.Items.Item[0]
    # print('ASIN---->:', item.ASIN.cdata)
    # print('Title---->', item.ItemAttributes.Title.cdata)


if __name__ == '__main__':
    # test()
    title = 'Apple MF839LL'
    keywords = title.replace('-', '').split()
    data = item_search(','.join(keywords))
    parse_data(data)
