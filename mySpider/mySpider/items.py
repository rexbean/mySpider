# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    accountName = scrapy.Field()
    date = scrapy.Field()


class ArticleItem(scrapy.Item):
    title       = scrapy.Field()
    date        = scrapy.Field()
    author      = scrapy.Field()
    accountName = scrapy.Field()
    accountId   = scrapy.Field()
    content     = scrapy.Field()
    
