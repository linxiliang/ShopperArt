"""Shopper Art Models."""
import datetime
from mongoengine import (
    Document, StringField, connect, DateTimeField, FloatField)
from shopperart.settings import DBNAME

connect(DBNAME)


class Product(Document):
    """Standard product info."""

    pid = StringField(max_length=20, required=True)
    title = StringField(max_length=256, required=True)
    image = StringField(max_length=256, required=True)
    shortDescription = StringField(max_length=256, required=True)
    create_time = DateTimeField(default=datetime.datetime.now)


class PriceHistory(Document):
    """Price history."""

    website = StringField(max_length=20, required=True)
    pid = StringField(max_length=20, required=True)
    price = FloatField(required=True)
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
