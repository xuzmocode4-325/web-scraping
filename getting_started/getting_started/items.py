# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class GettingStartedItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QuoteItem(Item):
    text = Field()
    author = Field()
    tags = Field()
