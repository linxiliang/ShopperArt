"""Script for crawling product prices from Best Buy."""
import time
import requests
from django.core.management.base import BaseCommand
from dumbhead.models import Product, PriceHistory


MAXPAGE = 5
BESTBUY = 'bestbuy'
HOST = 'https://api.bestbuy.com/v1/products(sku in({search}))?'
KEY = 'mQG1n4CF8F7YfvGtyAoMQdGY'
PARAM = 'format=json&apiKey={key}&show={show}'
SEARCH_URL = HOST + PARAM
ATTRIBUTES = ['source', 'salePrice', 'sku']


class Command(BaseCommand):
    """Command."""

    help = 'Command for getting categories'

    def handle(self, *args, **options):
        """Handle command."""
        pids = []
        products = list(Product.objects.all())
        for index, product in enumerate(products):
            if index % 10 == 0 and pids:
                print('getting====>', pids)
                self.get_products_price(pids)
                if index % 20 == 0:
                    time.sleep(1)
                pids = []
            else:
                pids.append(product.id)

    def get_products_price(self, pids):
        """Get products by category."""
        total_num = MAXPAGE
        num = 1
        while(num <= total_num):
            url = SEARCH_URL.format(
                key=KEY, show=','.join(ATTRIBUTES), search=','.join(pids))
            data = requests.get(url).json()
            if 'fault' in data or 'error' in data:
                print(data)
                num += 1
                continue
            for p_data in data['products']:
                pid = str(p_data['sku'])
                price_his = PriceHistory.objects.filter(
                    website=BESTBUY, pid=pid).first()
                if not price_his or price_his.salePrice != p_data['salePrice']:
                    PriceHistory(website=BESTBUY, pid=pid,
                                 salePrice=p_data['salePrice']).save()
            break
