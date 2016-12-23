"""Script for crawling amazon products."""
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
from dumbhead.models import Product, WebsiteProduct

AMAZON = 'amazon'
KEY = 'AKIAJIU4THDG4KYCA3KQ'
SECRET = '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'
URL = 'http://webservices.amazon.com/onca/xml?'
PARAMS = {
    'Service': 'AWSECommerceServic',
    'AWSAccessKeyId': KEY,
    'AssociateTag': 'isaac07b-20',
    'Operation': 'ItemSearch',
    'SearchIndex': 'All',
    'Timestamp': '',
}


class Command(BaseCommand):
    """Command."""

    help = 'Command for getting amazon products'

    def handle(self, *args, **options):
        """Handle command."""
        while True:
            web_pids = set([p.pid for p in WebsiteProduct.objects.all()])
            pids = set([p.id for p in Product.objects.all()
                        if p.modelNumber is not None])
            print('to crawl size---->', len(pids - web_pids))
            if not (pids - web_pids):
                break
            products = list(Product.objects.all())
            random.suffle(products)
            for product in products:
                if product.id in web_pids or not product.modelNumber:
                    continue
                keywords = [product.manufacturer, product.modelNumber]
                self.get_products(product.id, ','.join(keywords))

    def get_products(self, pid, keywords):
        """Get products by keywords."""
        params = copy.copy(PARAMS)
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
        flag = False
        count = 1
        while not flag and count <= 5:
            data = requests.get(URL + param_str)
            count += 1
            time.sleep(1)
            flag = self.parse_data(pid, data)
        if count >= 5:
            print('failed product----->', keywords, data.text)

    def parse_data(self, pid, data):
        """Parse xml data."""
        if 'ItemSearchErrorResponse' in data.text:
            return False
        root = untangle.parse(data.text)
        total_num = int(root.ItemSearchResponse.Items.TotalResults.cdata)
        if total_num == 1:
            item = root.ItemSearchResponse.Items.Item
        elif total_num > 1:
            item = root.ItemSearchResponse.Items.Item[0]
        else:
            return True
        wpid = item.ASIN.cdata
        name = item.ItemAttributes.Title.cdata
        print('ASIN---->:', wpid)
        print('Title---->', name)
        record = WebsiteProduct.objects.filter(website=AMAZON, pid=pid).first()
        if not record:
            WebsiteProduct(
                website=AMAZON, pid=pid, wpid=wpid, name=name).save()
        else:
            record.wpid = wpid
            record.name = name
            record.save()
        return True
