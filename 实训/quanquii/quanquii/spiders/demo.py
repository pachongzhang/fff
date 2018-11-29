# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.spiders.crawl import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from ..items import QuanquiiItem
class DemoSpider(CrawlSpider):
    name='demo'
    # allowed_domains = ['www']
    start_urls = ['http://www.dayinhu.com/news/category/%E7%A7%91%E6%8A%80%E5%89%8D%E6%B2%BF']
    rules=(
        Rule(LinkExtractor(allow=(r'http://www.dayinhu.com/news/category/%E7%A7%91%E6%8A%80%E5%89%8D%E6%B2%BF/page/\d+')), follow=True),
        Rule(LinkExtractor(allow=(r'http://www.dayinhu.com/news/\d{6}.html'),restrict_css=('h1.entry-title a')), callback="parse_items",follow=False),
    )
    def parse_items(self, response):
        aurl=response.url
        data=QuanquiiItem()
        # print(response.text)
        try:
            sel=Selector(response)
            if response.css('header.entry-header h1::text'):
                title=response.css('header.entry-header h1::text').extract()
            else:
                raise Exception('title is null')
            if response.css('time.entry-date ::text'):
                data_time = response.css('time.entry-date ::text').extract()
            else:
                data_time = ''
            if response.css('meta[name="description"]::attr(content)'):
                daodu = response.css('meta[name="description"]::attr(content)').extract()[0]
            else:
                daodu = ''
            if response.css('div.entry-content ').re('作者：.+'):
                author=response.css('div.entry-content ').re('作者：.+')[0].rstrip('</p>')
            else:
                author = ''
            if response.css('div.entry-content ').re('来源：.+'):
                laiyuan = response.css('div.entry-content ').re('来源：.+')[0].rstrip('</p>')
            else:
                laiyuan = ''
            if response.css('div.entry-content  p::text'):
                content = ''.join(response.css('div.entry-content  p::text').extract()).strip()
            else:
                content = ''
            if response.css('meta[name="keywords"]::attr(content)'):
                biaoqian = response.css('meta[name="keywords"]::attr(content)').extract()
            else:
                biaoqian = ''
            if response.css('div.entry-content  p img ::attr(src)'):
                img= response.css('div.entry-content  p img ::attr(src)').extract()
            else:
                img = ''

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
            if not os.path.exists('log'):
                os.mkdir('log')
            with open('log.text', encoding='utf-8')as f:
                f.write('{0}' + '\n' + '{1}'.format(e, aurl))
