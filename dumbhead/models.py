"""Shopper Art Models."""
import datetime
from mongoengine import (
    Document, StringField, connect, DateTimeField, FloatField,
    BooleanField)
from django.conf import settings

connect(settings.DBNAME)


class Category(Document):
    """Product category."""

    cid = StringField(max_length=20, required=True)
    name = StringField(max_length=256, required=True)
    searched = BooleanField(default=False)


class Product(Document):
    """Standard product info."""

    pid = StringField(max_length=20, required=True, primary_key=True)
    cid = StringField(max_length=20, required=True)
    upc = StringField(max_length=20, required=True)
    name = StringField(max_length=512, required=True)
    image = StringField(max_length=256, required=True)
    manufacturer = StringField(max_length=256)
    modelNumber = StringField(max_length=64)
    shortDescription = StringField(max_length=512)
    create_time = DateTimeField(default=datetime.datetime.now)


class WebsiteProduct(Document):
    """website product info."""

    website = StringField(max_length=20, required=True)
    pid = StringField(max_length=20, required=True)
    wpid = StringField(max_length=20, required=True)
    name = StringField(max_length=512, required=True)
    searched = BooleanField(default=False)
    create_time = DateTimeField(default=datetime.datetime.now)


class PriceHistory(Document):
    """Price history."""

    website = StringField(max_length=20, required=True)
    pid = StringField(max_length=20, required=True)
    salePrice = FloatField(required=True)
    create_time = DateTimeField(default=datetime.datetime.now)


class ItemReview(Document):
    """Item review from different website."""

    website = StringField(max_length=20, required=True)
    pid = StringField(max_length=20, required=True)
    content = StringField(max_length=256, required=True)
    create_time = DateTimeField(default=datetime.datetime.now)


class Filter(Document):
    """Search content."""

    category = StringField(max_length=20, required=True)
