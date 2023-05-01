# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http import Request

class WikilocSpiderSpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = ['wikiloc.com']
    start_urls = ['https://www.wikiloc.com/trails/france/auvergne-rhone-alpes']   #your link
    liste = []
    def parse(self, response):
        villes = response.xpath('//div[@id="filters"]/ul/li/a/@href').extract()
        for v in villes :
            yield Request(v, self.parse_detail)
    def parse_detail(self, response):
        trails = response.xpath('//ul[@class="trail-list"]/li')
        next = response.xpath('//a[@class="next"]/@href').extract_first()
        for t in trails:
            link = t.xpath('./div/div/h3/a/@href').extract_first()
            if link is not None:
                item={}
                item["Link"] = link
                yield item
        if next is not None:
            base = response.url.split('?')[0]
            next_page = base + next
            yield Request(next_page, self.parse_detail)
