#!/usr/bin/python
# -*- coding:utf-8 -*-

import scrapy
import re
import urllib2

from config import proxyList
from scrapy.selector import Selector
from mySpider.items import IPItem
from Utility.utility import Utility
from Utility.validateIp import ValidateIp



class IPSpider(scrapy.Spider):

    # name = "ip"
    # urls = []
    # allowed_domains = [
    #     # the website of proxy list
    #     "xicidaili.com",
    #     "66ip.cn"
    # ]

    name = "IpSpider"
    urls = []
    allowed_domains = ["free-proxy-list.net"]

    start_urls = [
        "https://free-proxy-list.net"
    ]

    def parse(self, response):

    # def start_requests(self):
    #     url = proxyList[2]['url'][0]
    #     print url
    #     yield scrapy.Request(url,meta={'p':proxyList[2]},callback=self.parse)

        ipItem = IPItem()
        i = 0


        list = re.findall("<tr><td>(.*?)<\/td><td>(.*?)<\/td><td>.*?<\/td><td class='hm'>.*?<\/td><td>(.*?)<\/td><td class='hm'>.*?<\/td><td class='hx'>.*?<\/td><td class='hm'>.*?<\/td><\/tr>",response.body)
        file_object = open('thefile.txt', 'w')
        for u in list:
            ip =  u[0]
            port =u[1]
            anonymous =u[2]


        # proxy       = response.meta['p']
        # rootPath    = proxy['root']
        # table       = response.xpath(rootPath).extract()
        #
        # for sel in Selector(response=response).xpath(rootPath):
        #     ipPath      = proxy['ip']
        #     portPath    = proxy['port']
        #
        #     ipList      = sel.xpath(ipPath).extract()
        #     portList    = sel.xpath(portPath).extract()
        #
        #     ip          = Utility.listToStr(ipList)
        #     port        = Utility.listToStr(portList)

            # using regular expression to validate whether it is a valid ip
            regex       = '\d.{1,3}\d{1,3}'
            if re.match(regex, ip):
                v = ValidateIp()
                protocol, anonymous, speed =  v.validate(ip,port)
                if protocol is not -1:
                    i = i+1
                    ipItem['ip']    = ip
                    ipItem['port']  = port
                    print ipItem['ip'],':',ipItem['port']

                    file_object.write(str(i) + "   " + ip + ":" + port)

                else:
                    continue
            else:
                continue
        file_object.close( )
