# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pandas as pd
import requests

class WikilocSpiderSpider(scrapy.Spider):
    name = 'wikiloc_image'
    allowed_domains = ['wikiloc.com']
    start_urls = list(pd.read_csv("link.csv")["Link"])

    def parse(self, response):
        item = {}
        js = json.loads(response.xpath('//script[@type="application/ld+json"]').extract()[1].replace('\n','').replace('\t','').replace('<script type="application/ld+json">','').replace('</script>',''))
        item['url_track'] = response.url
        item['track name'] = response.xpath('//h1[@class="d-inline dont-break-out"]/text()').extract_first().strip().replace(';',',')
        item['user_name'] = response.xpath('//div[@class="user-info"]/h3/a/text()').extract_first().replace(';',',')
        item['Date'] =  js['datePublished']
        images = response.xpath('//div[@class="simplecard"]')
        for im in images:
            link = im.xpath('./div[@class="simplecard__description"]/ul/li/a/img/@data-src').extract_first()
            if link is not None:
                item['Id_images'] = im.xpath('./@id').extract_first()
                item['url_images'] =  link.replace('_tn','')
                long_lat= im.xpath('./div[@class="simplecard__footer clearfix"]/div/span/@title').extract_first()
                if long_lat is not None: 
                    item['latitude'] = long_lat.split(':')[1].split('\n')[0].strip()
                    item['longitude'] = long_lat.split(':')[1].split('\n')[1].strip()
                    yield item
