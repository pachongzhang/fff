# -*- coding: utf-8 -*-
import scrapy,re
import json
from newspaper import Article
class K36Spider(scrapy.Spider):
    name = 'k36'
    # allowed_domains = ['www.']
    start_urls = ['https://36kr.com/api/search-column/mainsite?per_page=20&page=2']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    }
    # def start_requests(self):
    #     url='https://36kr.com/api/search-column/mainsite?per_page=20&page=2'
    def parse(self, response):
        data=json.loads(response.text).get('data').get('items')
        for i in data:
            p_id=i.get('id')
            title=i.get('title')
            time=i.get('published_at')
            url = 'https://36kr.com/p/{}.html'.format(p_id)
            if i.get('column_name')=='氪视频':
                url = 'https://36kr.com/video/{}.html'.format(p_id)

            else:
                pass
            yield scrapy.Request(url, self.detail,meta={'title':title,'time':time})
    def detail(self, response):
        conten=re.findall('<p>(.*?)</p>',response.text,re.S)
        biaoqian=response.xpath('//*[@name="keywords" ]/@content').extract()
        print(biaoqian,conten)

