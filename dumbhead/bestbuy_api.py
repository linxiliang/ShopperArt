"""API for Best Buy."""
import requests

HOST = 'https://api.bestbuy.com/v1/products'
KEY = 'mQG1n4CF8F7YfvGtyAoMQdGY'
EXTRA = '&format=json&&sort=salesRankMediumTerm.asc'
SEARCH_URL = HOST + '({search})?show={show}&apiKey={key}' + EXTRA
ITEM_URL = HOST + '/{sku}.json?apiKey={key}&show={show}'
ATTRIBUTES = ['sku', 'name', 'salePrice', 'shortDescription']


def keyword_search(keywords):
    """Search by keywords."""
    search = '|'.join(['search={key}'.format(key=key) for key in keywords])
    url = SEARCH_URL.format(search=search, show=','.join(ATTRIBUTES), key=KEY)
    data = requests.get(url)
    return data.json()['products']


def item_lookup(sku):
    """Look up item."""
    url = ITEM_URL.format(sku=sku, key=KEY, show=','.join(ATTRIBUTES))
    data = requests.get(url)
    return data.json()


if __name__ == '__main__':
    print(item_lookup('6443034'))
    data = keyword_search(['iphone', 'ipad'])
    print(data)
