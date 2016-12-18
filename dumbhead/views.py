"""Dumbhead views."""
import json
from django.http import HttpResponse
from .bestbuy_api import item_lookup, keyword_search


def index(request):
    """Index."""
    return HttpResponse("Hello, world. You're at the dumbhead index.")


def item(request):
    """Display item detail."""
    sku = request.GET['sku']
    data = item_lookup(sku)
    return HttpResponse(json.dumps(data), content_type="application/json")


def search(request):
    """Search things."""
    # search = request.GET['keywords'].split()
    data = keyword_search(['iphone', 'ipad'])
    return HttpResponse(json.dumps(data), content_type="application/json")
