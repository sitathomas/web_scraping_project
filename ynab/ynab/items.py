# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YnabItem(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    user = scrapy.Field()
    posted = scrapy.Field()
    text = scrapy.Field()
    replies = scrapy.Field()
    likes = scrapy.Field()
    views = scrapy.Field()
    following = scrapy.Field()
