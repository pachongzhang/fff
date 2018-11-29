# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders.crawl import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
import os
import json
from ..items import QuanquiiItem
from scrapy.selector import Selector
import time
class JingdongSpider(CrawlSpider):
    name = 'jingdong'
    # allowed_domains = ['www']
    start_urls = ['https://search.jd.com/Search?keyword=%E9%A3%9E%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=f&stock=1&page='+str(2*n-1) +'&click=0'for n in range(1,10)]
    # rules = (
    #     # Rule(LinkExtractor(allow=(r'http://www.81uav.cn/uav-news/4_\d+.html')),follow=True),
    #     # 'http://tech.163.com/18/1128/13/E1N1NM0D00099968.html'
    #     Rule(LinkExtractor(allow=(r'https://item.jd.com/\d+.html')), callback="parse_items",follow=False),
    # )
    def parse(self, response):
       list=response.xpath('//li[contains(@class,"gl-item")]')
       for ite in list:
           price=ite.xpath('div/div[2]/strong/i/text()').extract()
           title=''.join(ite.xpath('div/div[3]/a//text()').extract()).strip()
       # page = response.url.split('&page=')[1].split('&click')[0]
       good_id = ''.join(response.xpath('//*[@id="J_goodsList"]/ul/li/@data-sku').extract()).strip()
       a=time.time()
       for n in range(1,10):
            url='https://search.jd.com/s_new.php?keyword=%E9%A3%9E%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=f&stock=1&page='+str(2*n)+'4&s=81&scrolling=y&log_id='+str(a)+'&tpl=1'
            yield scrapy.Request(url,self.show)
    def show(self, response):
        list = response.xpath('//li[contains(@class,"gl-item")]')
        for ite in list:
            price = ite.xpath('div/div[2]/strong/i/text()').extract()
            title = ''.join(ite.xpath('div/div[3]/a//text()').extract()).strip()
            print(price,title)
        # listss = [i.replace('<font class="skcolor_ljg">', '').replace('</font>', '') for i in lists]


