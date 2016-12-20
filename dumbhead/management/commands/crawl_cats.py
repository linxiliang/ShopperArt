"""Script for crawling cats from Best Buy."""
import time
import requests
from django.core.management.base import BaseCommand
from dumbhead.models import Category

HOST = 'https://api.bestbuy.com/v1/categories?format=json&show=all&'
KEY = 'mQG1n4CF8F7YfvGtyAoMQdGY'
SIZE = 100
PARAM = 'apiKey={key}&pageSize={size}&page={num}'


class Command(BaseCommand):
    """Command."""

    help = 'Command for getting categories'

    def handle(self, *args, **options):
        """Handle command."""
        Category.objects.delete()
        total_num = 10
        num = 1
        while(num <= total_num):
            url = HOST + PARAM.format(key=KEY, size=SIZE, num=num)
            print('=====>', url)
            data = requests.get(url).json()
            if 'fault' in data or 'error' in data:
                print('---->', data)
                continue
            total_num = data['totalPages']
            for cat_data in data['categories']:
                if 'name' not in cat_data or not cat_data['name']:
                    continue
                record = Category.objects.filter(cid=cat_data['id']).first()
                if not record:
                    record = Category(
                        cid=cat_data['id'], name=cat_data['name']).save()
                else:
                    record.name = cat_data['name']
                    record.save()
            num += 1
            if num % 2 == 0:
                time.sleep(1)
