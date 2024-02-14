# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MulchItem(scrapy.Item):
    url = scrapy.Field()
    text = scrapy.Field()
    keywords = scrapy.Field()
