# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pandas as pd

class WikilocSpiderSpider(scrapy.Spider):
    name = 'wiki_track'
    allowed_domains = ['wikiloc.com']
    start_urls = list(pd.read_csv("link.csv")["Link"])

    def parse(self, response):
        item = {}
        js = json.loads(response.xpath('//script[@type="application/ld+json"]').extract()[1].replace('\n','').replace('\t','').replace('<script type="application/ld+json">','').replace('</script>',''))
        item['track name'] = response.xpath('//h1[@class="d-inline dont-break-out"]/text()').extract_first().strip().replace(";",',')
        item['track .gpx'] = ""	
        item['Track type'] = response.xpath('//div[@class="crumbs display"]/strong/text()').extract_first()
        item['Difficulty'] = response.xpath('//a/@title[contains(.,"difficulty")]').extract_first().split(':')[1].strip()
        Distance = response.xpath('//a/@title[contains(.,"Distance")]').extract_first().split('Distance')[1].replace(',','.')
        if '.' in Distance:
            if "nautical" not in Distance:
                conv_fac = 0.621371
                d = re.findall("\d+\.\d+", Distance)[0]
                item['Distance'] = "{:.2f}".format(float(d) / float(conv_fac))
            elif "nautical" in Distance:
                conv_fac = 0.539957
                d = re.findall("\d+\.\d+", Distance)[0]
                item['Distance'] = "{:.2f}".format(float(d) / float(conv_fac))
        else:
            if "nautical" not in Distance:
                conv_fac = 0.621371
                d = re.findall("\d+", Distance)[0]
                item['Distance'] = "{:.2f}".format(int(d) / float(conv_fac))
            elif "nautical" in Distance:
                conv_fac = 0.539957
                d = re.findall("\d+", Distance)[0]
                item['Distance'] = "{:.2f}".format(int(d) / float(conv_fac))
        item['Date'] = 	js['datePublished']
        item['Author'] = response.xpath('//div[@class="user-info"]/h3/a/text()').extract_first().replace(";",',')
        vd = response.xpath('//div[@class="trail-hits"]/p/text()').extract()
        item['viewed'] = ''.join(re.findall(r'\d+',vd[0]))	
        item['downloaded'] = ''.join(re.findall(r'\d+',vd[1]))
        item['description text'] = response.xpath('//meta[@name="description"]/@content').extract_first().replace('\n','').replace('\t','').replace('\r','').strip().replace(";",',')
        item['url_track'] = response.url
        yield item
