"""Script for crawling amazon prices."""
import copy
import hmac
import time
import random
import base64
import hashlib
import urllib
import requests
import untangle
from django.core.management.base import BaseCommand
from dumbhead.models import WebsiteProduct, PriceHistory

AMAZON = 'amazon'
KEY = 'AKIAJIU4THDG4KYCA3KQ'
SECRET = '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'
URL = 'http://webservices.amazon.com/onca/xml?'
PARAMS = {
    'Service': 'AWSECommerceServic',
    'AWSAccessKeyId': KEY,
    'AssociateTag': 'isaac07b-20',
    'Operation': 'ItemLookup',
    'Timestamp': '',
    'ResponseGroup': 'Offers',
}


class Command(BaseCommand):
    """Command."""

    help = 'Command for getting amazon products'

    def handle(self, *args, **options):
        """Handle command."""
        while True:
            products = list(WebsiteProduct.objects.filter(
                searched=False, website=AMAZON).all())
            if not products:
                break
            random.shuffle(products)
            for product in products:
                flag = self.get_products(product.pid, product.wpid)
                if flag:
                    product.searched = True
                    product.save()

    def get_products(self, pid, wpid):
        """Get products by keywords."""
        params = copy.copy(PARAMS)
        params['ItemId'] = wpid
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
        flag = False
        count = 1
        while not flag and count <= 5:
            data = requests.get(URL + param_str)
            count += 1
            time.sleep(1)
            flag = self.parse_data(pid, data)
        if count >= 5:
            print('failed product----->', data.text)
        return flag

    def parse_data(self, pid, data):
        """Parse xml data."""
        if 'ItemSearchErrorResponse' in data.text:
            return False
        root = untangle.parse(data.text)
        try:
            sale_price = float(root.ItemLookupResponse.Items.Item.OfferSummary
                               .LowestNewPrice.FormattedPrice.cdata[1:])
        except Exception:
            print(data.text)
            return True
        print(pid, '---price->', sale_price)
        record = PriceHistory.objects.filter(website=AMAZON, pid=pid).first()
        if not record:
            PriceHistory(
                website=AMAZON, pid=pid, salePrice=sale_price).save()
        else:
            record.salePrice = sale_price
            record.save()
        return True
