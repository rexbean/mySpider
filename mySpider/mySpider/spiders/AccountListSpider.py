#!/usr/bin/python
# -*- coding:utf-8 -*-

import scrapy
import subprocess

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from mySpider.items import AccountListItem
from mySpider.items import ArticleListItem
from mySpider.spiders.ArticleSpider import ArticleSpider

from Utility.utility import Utility

class AccountListSpider(scrapy.Spider):

    name = "accountList"
    urls = []
    allowed_domains = ["qq.com"]
    accountListConst = '11002301'

    start_urls = [
        # type:
        # 1 is for account
        # 2 is for article
        "http://weixin.sogou.com/weixin?type=1&query=大数据"

    ]

    def parse(self,response):
        response = response.replace(body=response.body.replace('<em>', ''))
        for n in range(1):
            accountListItem = AccountListItem()
            num             = self.accountListConst

            '''
            //*[@id="sogou_vr_11002301_box_0"]/dl[1]/dd/text()[1]
            //*[@id="sogou_vr_11002301_box_0"]/dl[2]/dd
            //*[@id="sogou_vr_11002301_box_0"]/dl[3]/dd/a
            //*[@id="sogou_vr_11002301_box_7"]/div/div[2]/p[2]/text()[2]
            '''

            rootPath        = '//*[@id="sogou_vr_'+num+'_box_'+str(n)+'"]'
            accountIdPath   = './div/div[2]/p[2]/label//text()'
            functionPath    = './dl[1]/dd//text()'
            authenticatePath= './dl[2]/dd//text()'
            latestArticleP  = './dl[3]/dd/a'

            txtBox          = response.xpath(rootPath)
            function        = txtBox.xpath(functionPath).extract()
            authenticate    = txtBox.xpath(authenticatePath).extract_first()
            latestArticleN  = txtBox.xpath(latestArticleP + "//text()").extract_first()
            latestArticleL  = txtBox.xpath(latestArticleP + "/@href").extract_first()

            accountId       = txtBox.xpath(accountIdPath).extract_first()
            accountName     = txtBox.xpath('./div/div[2]/p[1]/a//text()').extract_first()

            url             = txtBox.xpath('./div/div[2]/p[1]/a/@href').extract_first()
            url             = url.replace('http','https')

            accountListItem['accountName']   = Utility.listToStr(accountName)
            accountListItem['url']           = url
            accountListItem['accountId']     = accountId.encode('utf-8')
            accountListItem['function']      = Utility.listToStr(function).encode('utf-8')
            accountListItem['authenticate']  = authenticate
            accountListItem['latestArticleN']= latestArticleN
            accountListItem['latestArticleL']= latestArticleL

            cmd = "phantomjs ../Utility/getBody.js '%s'" % url
            print "cmd===",cmd

            stdout, stderr =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE).communicate()
            r = HtmlResponse(url=url, body=stdout)

            articleUrls = self.parseAccount(r)
            for url in articleUrls:
                yield scrapy.Request(url, callback=ArticleSpider().parse)



            print "=======================Account======================="
            print "accountName==",   accountListItem['accountName']
            print "url==",           accountListItem['url']
            print "accountId==",     accountListItem['accountId']
            print "function==",      Utility.listToStr(function).encode('utf-8')
            print "authenticate==",  authenticate
            print "latestArticleN==",latestArticleN
            print "latestArticleL==",latestArticleL



            # JavaScript is used in numperMon, work on it later
            # numPerMonPath   = './div/div[2]/p[2]//text()'
            # numPerMon       = txtBox.xpath(numPerMonPath).extract()
            # if numPerMon is None:
            #     numPerMon = ''
            # else:
            #     numPerMon = Utility.listToStr(numPerMon).encode('utf-8')
            # print "numperMon==",     numPerMon

    def parseAccount(self,response):
        urls = []

        articleListItem =  ArticleListItem()
        title = response.xpath('/html/head/title//text()').extract()
        print Utility.listToStr(title)

        print '========================account======================='
        for articlePath in Selector(response=response).xpath('//*[@class="weui_media_box appmsg"]/div'):
            # title
            title = articlePath.xpath('./h4//text()').extract()[0].strip()
            articleListItem['title'] = title
            print articleListItem['title']
            # url
            url = articlePath.xpath('./h4//@hrefs').extract()[0]
            url = "https://mp.weixin.qq.com"+url
            articleListItem['url'] = url

            print articleListItem['url']
            # date
            date = articlePath.xpath('.//*[@class="weui_media_extra_info"]//text()').extract()[0]
            articleListItem['date'] = date
            print articleListItem['date']
            # abstract
            summary = articlePath.xpath('.//*[@class="weui_media_desc"]//text()').extract()
            articleListItem['summary'] = Utility.listToStr(summary)
            print articleListItem['summary']
            urls.append(url)

        return urls
