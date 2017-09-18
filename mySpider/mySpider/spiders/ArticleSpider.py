#!/usr/bin/python
# -*- coding:utf-8 -*-

import scrapy

from scrapy.selector import Selector

from mySpider.items import ArticleItem
from Utility.utility import Utility

# the spider to get the articleList
class ArticleSpider(scrapy.Spider):
