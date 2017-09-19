#!/usr/bin/python
# -*- coding:utf-8 -*-

import scrapy

from scrapy.selector import Selector

from mySpider.items import ArticleItem
from Utility.utility import Utility

# the spider to get the articleList
class ArticleSpider(scrapy.Spider):
    name = "article"
    urls = []

    def parse(self,response):
        articleItem = ArticleItem()

        title       = response.xpath('//*[@id="activity-name"]//text()').extract_first().strip()
        date        = response.xpath('//*[@id="post-date"]//text()').extract_first()
        author      = response.xpath('//*[@id="img-content"]/div[1]/em[2]//text()').extract_first()
        accountName = response.xpath('//*[@id="post-user"]//text()').extract_first()
        accountId   = response.xpath('//*[@id="js_profile_qrcode"]/div/p[1]/span//text()').extract_first()
        content     = response.xpath('//*[@id="js_content"]').extract()

        articleItem['title']        = title.encode('utf-8')
        articleItem['date']         = date.encode('utf-8')
        articleItem['accountName']  = accountName.encode('utf-8')
        articleItem['accountId']    = accountId.encode('utf-8')
        articleItem['content']      = Utility.listToStr(content).encode('utf-8')

        if author is None:
            author = ''
        else:
            author = author

        articleItem['author']   = author

        print "======================article========================"
        print "title== ",       articleItem['title']
        print "date== ",        articleItem['date']
        print "author== ",      articleItem['author']
        print "accountName== ", articleItem['accountName']
        print "accountId== ",   articleItem['accountId']
        print "content"
        # print articleItem['content']

        yield articleItem
