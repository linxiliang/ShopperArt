"""Script for crawling bhphotovideo products."""
import time
import random
import requests
from pyquery import PyQuery
from django.core.management.base import BaseCommand
from dumbhead.models import Product, WebsiteProduct, PriceHistory

HOST = 'https://www.bhphotovideo.com/c/search?Ntt={keywords}'
BP = 'bhphotovideo'


class Command(BaseCommand):
    """Command."""

    help = 'Command for getting amazon products'

    def handle(self, *args, **options):
        """Handle command."""
        while True:
            web_pids = set([p.pid for p in
                            WebsiteProduct.objects.filter(website=BP).all()])
            pids = set([p.id for p in Product.objects.all()
                        if p.modelNumber is not None])
            print('to crawl size---->', len(pids - web_pids))
            if not (pids - web_pids):
                break
            products = list(Product.objects.all())
            random.shuffle(products)
            for product in products:
                if product.id in web_pids or not product.modelNumber:
                    continue
                keywords = [product.manufacturer, product.modelNumber]
                self.get_products(product.id, keywords)
                time.sleep(1)

    def get_products(self, pid, keywords):
        """Get products by keywords."""
        try:
            re = PyQuery(url=HOST.format(keywords='+'.join(keywords)))
            wpid = re('.sku')[0].text
            brand = re('.bold.fourteen')('span')[0].text
            title = re('.bold.fourteen')('span')[1].text
            price = float(re('.price')[0].text.strip()[1:])
        except Exception as e:
            print(HOST.format(keywords='+'.join(keywords)), e)
            data = requests.get(HOST.format(keywords='+'.join(keywords)))
            if data.status_code == 403:
                print(data.text)
            return
        name = brand + ' ' + title
        print('get---->', pid, name, price)
        record = WebsiteProduct.objects.filter(website=BP, pid=pid).first()
        if not record:
            WebsiteProduct(
                website=BP, pid=pid, wpid=wpid, name=name[:512]).save()
        else:
            record.wpid = wpid
            record.name = name
            record.save()
        record = PriceHistory.objects.filter(website=BP, pid=pid).first()
        if not record:
            PriceHistory(website=BP, pid=pid, salePrice=price).save()
        else:
            record.salePrice = price
            record.save()
