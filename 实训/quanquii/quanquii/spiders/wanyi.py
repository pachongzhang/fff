# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders.crawl import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
import os
import json
from ..items import QuanquiiItem
from scrapy.selector import Selector
class WanyiSpider(CrawlSpider):
    name = 'wanyi'
    # allowed_domains = ['www']
    start_urls = ['http://tech.163.com/gd/']
    rules = (
        # Rule(LinkExtractor(allow=(r'http://www.81uav.cn/uav-news/4_\d+.html')),follow=True),
        # 'http://tech.163.com/18/1128/13/E1N1NM0D00099968.html'
        Rule(LinkExtractor(allow=(r'http://tech.163.com/special/gd2016_\d{2}/')),follow=True),
        Rule(LinkExtractor(allow=(r'http://tech.163.com/\d{2}/\d{4}/\d{2}/\w{16}.html')), callback="parse_items",follow=False),
    )
    # def parse(self, response):
    #     for i in json.loads(response.body.decode('gbk').strip('data_callback(').strip(')')):
    #         tlink=i.get('tlink')
    #         yield scrapy.Request(tlink,self.show)
    def parse_items(self, response):
        data=QuanquiiItem()
        try:
            if response.css('#epContentLeft > h1::text'):
                title=response.css('#epContentLeft > h1::text').extract()
            else:
                raise Exception('title is none')
            if response.css('div.post_time_source ::text').re('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'):
                data_time=response.css('div.post_time_source ::text').re('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')[0]
            else:
                data_time=''
            if response.css('.post_time_source a::text'):
                laiyuan=response.css('.post_time_source a::text').extract_first()
            else:
                laiyuan=''
            if response.css('#endText > div.ep-source.cDGray > span.ep-editor::text'):
                authors=response.css('#endText > div.ep-source.cDGray > span.ep-editor::text').extract_first()
                author=authors.replace('责任编辑：','')
            else:
                author=''
            if response.css('div.post_text p::text'):
                content=''.join(response.css('div.post_text p::text').extract()).strip()
            else:
                content=''
            if response.css('div.post_text p img::attr(src)'):
                img=response.css('div.post_text p img::attr(src)').extract()
            else:
                img=''
            if response.css('meta[name="description"] ::attr(content)'):
                daodu=response.css('meta[name="description"] ::attr(content)').extract()
            else:
                daodu=''
            if response.css('meta[name="keywords"] ::attr(content)'):
                biaoqian=response.css('meta[name="keywords"] ::attr(content)').extract()
            else:
                biaoqian=''
            data['daodu'] = daodu
            data['title'] = title
            data['data_time'] = data_time
            data['lai'] = laiyuan
            data['authors'] = author
            data['biaoqian'] = biaoqian
            data['img'] = img
            data['content'] = content
            # data['lianjie'] = lianjie
            yield data
        except Exception as e:
            pass