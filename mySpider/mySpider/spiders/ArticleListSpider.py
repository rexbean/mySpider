#!/usr/bin/python
# -*- coding:utf-8 -*-

import scrapy

from scrapy.selector import Selector

from mySpider.items import ArticleListItem
from mySpider.spiders.ArticleSpider import ArticleSpider
from Utility.utility import Utility

# the spider to get the articleList
class ArticleListSpider(scrapy.Spider):

    name = 'articleList'
    allowed_domains = ['qq.com']
    articleListConst = '11002601'

    start_urls = [
        # type: 1 is for account
        #       2 is for article
        "http://weixin.sogou.com/weixin?type=2&query=大数据"
    ]

    def parse(self, response):
        for n in range(10):
            articleListItem = ArticleListItem()
            num = self.articleListConst

            rootPath = '//*[@id="sogou_vr_' + num

            titlePath   = rootPath + '_title_'   + str(n) + '"]'
            summaryPath = rootPath + '_summary_' + str(n) + '"]'
            accountPath = rootPath + '_account_' + str(n) + '"]'
            datePath    = rootPath + '_box_'     + str(n) + '"]/div[2]/div/span'
            datePath_alt= rootPath + '_box_'     + str(n) + '"]/div/div[2]/span'

            '''
            # the xpath for two kind of article
            //*[@id="sogou_vr_11002601_box_1"]/div[2]/div/span/text()
            //*[@id="sogou_vr_11002601_box_9"]/div/div[2]/span/text()
            '''

            title       = response.xpath(titlePath   + '//text()').extract()
            url         = response.xpath(titlePath   + '/@href').extract_first()
            summary     = response.xpath(summaryPath + '//text()').extract()
            accountName = response.xpath(accountPath + '//text()').extract_first()

            '''
            # Javascript is used to get date
            # it may slow the process
            # so do it later
            date        = response.xpath(datePath    + '//text()').extract_first()

            if date is None:
                date    = response.xpath(datePath_alt+ '//text()').extract_first()
            print date
            '''

            articleListItem['url']          = url
            # articleListItem['date']         = date
            articleListItem['accountName']  = accountName
            articleListItem['title']        = Utility.listToStr(title)
            articleListItem['summary']      = Utility.listToStr(summary)

            print '=======================result======================'
            print 'title==' + articleListItem['title']
            print 'url=='   + articleListItem['url']
            print 'accountName==' + articleListItem['accountName']
            # print 'date==' + articleListItem['date']
            print 'summary'
            print articleListItem['summary']

            yield scrapy.Request(url, callback=ArticleSpider().parse)
