"""Script for crawling cats from Best Buy."""
import time
import requests
from django.core.management.base import BaseCommand
from dumbhead.models import Category, Product

SIZE = 100
MAXPAGE = 50
HOST = 'https://api.bestbuy.com/v1/products({search})?'
KEY = 'mQG1n4CF8F7YfvGtyAoMQdGY'
EXTRA = '&format=json&sort=salesRankMediumTerm.asc'
PARAM = 'show={show}&apiKey={key}&pageSize={size}&page={num}'
SEARCH_URL = HOST + PARAM + EXTRA
ATTRIBUTES = ['sku', 'name', 'upc', 'shortDescription', 'image', 'modelNumber',
              'manufacturer']


class Command(BaseCommand):
    """Command."""

    help = 'Command for getting categories'

    def handle(self, *args, **options):
        """Handle command."""
        cats = list(Category.objects.filter(searched=False))
        for cat in cats:
            print('getting====>', cat.to_json())
            self.get_products_cat(cat.cid)
            cat.searched = True
            print(cat.to_json())
            cat.save()

    def get_products_cat(self, cat_id):
        """Get products by category."""
        total_num = MAXPAGE
        num = 1
        while(num <= total_num):
            url = SEARCH_URL.format(
                key=KEY, size=SIZE, num=num, show=','.join(ATTRIBUTES),
                search='categoryPath.id={cat_id}'.format(cat_id=cat_id))
            data = requests.get(url).json()
            print('=====>', url, data.keys())
            if 'fault' in data or 'error' in data:
                print('---->', data)
                continue
            total_num = min(MAXPAGE, data['totalPages'])
            for product in data['products']:
                cur_data = {key: product.get(key, None)
                            for key in ATTRIBUTES[1:]}
                cur_data['cid'] = cat_id
                if not (cur_data['image'] and cur_data['upc'] and
                        cur_data['name']):
                    continue
                desc = cur_data['shortDescription']
                if desc and len(desc) > 512:
                    cur_data['shortDescription'] = desc[:512]
                pid = str(product['sku'])
                record = Product.objects.filter(pid=pid).first()
                if not record:
                    cur_data['pid'] = pid
                    record = Product(**cur_data).save()
                else:
                    record.update(**cur_data)
                    record.save()
            num += 1
            if num % 2 == 0:
                time.sleep(1)
