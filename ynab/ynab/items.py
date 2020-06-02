# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YnabItem(scrapy.Item):
    title = scrapy.Field()
    user = scrapy.Field()
    posted = scrapy.Field()
    category = scrapy.Field()
    replies = scrapy.Field()
    views = scrapy.Field()
    last_active = scrapy.Field()
    text = scrapy.Field()