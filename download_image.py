import requests
import pandas as pd
import scrapy


class DirectrSpider(scrapy.Spider):
    name = "download"
    start_urls = list(pd.read_csv("wikiloc_image.csv",sep= ";",low_memory=False,dtype = object)['url_images'])
    def response_is_ban(self, request, response):
        ban = (response.status_code != 200)
        url = request.meta.get('redirect_urls', [request.url])[0] if request.meta else request.url
        logger.debug("[RESPONSE_IS_BAN] %s, response.status=%s, response.url=%s, requested url=%s" %
        (str(ban),str(response.status),response.url,url))
        return ban
    def parse(self,response):
        response1 = requests.get(response.url,stream=True)
        if response1.status_code == 200:
            filename ="wp-" + '-'.join(response.url.split('/')[-2:])
            with open('./track_images/{}'.format(filename), 'wb') as f:
                f.write(response1.content)

