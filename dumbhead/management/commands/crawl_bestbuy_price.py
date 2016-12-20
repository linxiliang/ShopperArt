"""Script for crawling product prices from Best Buy."""
import time
import requests
from django.core.management.base import BaseCommand
from dumbhead.models import Product, PriceHistory


MAXPAGE = 5
BESTBUY = 'bestbuy'
HOST = 'https://api.bestbuy.com/v1/products/'
KEY = 'mQG1n4CF8F7YfvGtyAoMQdGY'
PARAM = '{sku}.json?apiKey={key}&show={show}'
SEARCH_URL = HOST + PARAM
ATTRIBUTES = ['source', 'salePrice']


class Command(BaseCommand):
    """Command."""

    help = 'Command for getting categories'

    def handle(self, *args, **options):
        """Handle command."""
        for index, product in enumerate(Product.objects.all()):
            print('getting====>', product.to_json())
            self.get_products_price(product.id)
            if index % 2 == 0:
                time.sleep(1)

    def get_products_price(self, pid):
        """Get products by category."""
        total_num = MAXPAGE
        num = 1
        while(num <= total_num):
            url = SEARCH_URL.format(
                key=KEY, show=','.join(ATTRIBUTES), sku=pid)
            data = requests.get(url).json()
            if 'fault' in data or 'error' in data:
                print(data)
                num += 1
                continue
            price_his = PriceHistory.objects.filter(
                website=BESTBUY, pid=pid).first()
            if not price_his or price_his.salePrice != data['salePrice']:
                PriceHistory(website=BESTBUY, pid=pid,
                             salePrice=data['salePrice']).save()
            break
