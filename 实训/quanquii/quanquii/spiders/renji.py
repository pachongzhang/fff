# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders.crawl import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
import os
from ..items import QuanquiiItem
from scrapy.selector import Selector
class RenjiSpider(CrawlSpider):
    name = 'renji'
    # allowed_domains = ['www']
    start_urls = ['http://www.81uav.cn/uav-news/4.html']
    rules = (
        # Rule(LinkExtractor(allow=(r'http://www.81uav.cn/uav-news/4_\d+.html')),follow=True),
        Rule(LinkExtractor(allow=(r'http://www.81uav.cn/uav-news/\d+/\d+/\d+.html'),restrict_css=('div.news-list-box a')), callback="parse_items",follow=False),
    )
    def parse_items(self, response):
        data=QuanquiiItem()
        aurl = response.url
        try:
            if response.css('body > div.m.mt15 > div.news_left > h1::text'):
                title=response.css('body > div.m.mt15 > div.news_left > h1::text').extract_first()
            else:
                raise Exception('title is none')
            if response.css('div.info::text').re('\d{4}-\d{2}-\d{2}')[0]:
                data_time=response.css('div.info::text').re('\d{4}-\d{2}-\d{2}')[0]
            else:
                data_time=''
            if response.css('div.info::text').re('来源：\w+'):
                laiyuan = response.css('div.info::text').re('来源：\w+')[0]
                lai = laiyuan.replace('来源：', '')
            else:
                lai = ''
            if response.css('div.info::text').re('作者：.*'):
                author = response.css('div.info::text').re('作者：.*')[0]
                authors = author.replace('作者：', '')
            else:
                authors = ''
            if response.css('body > div.m.mt15 > div.news_left > div.view > div:nth-child(9) > a::text'):
                biaoqian = response.css(
                    'body > div.m.mt15 > div.news_left > div.view > div:nth-child(9) > a::text').extract_first()
            else:
                biaoqian = ''
            if response.css('#article > p > img::attr(src)'):
                img = response.css('#article > p > img::attr(src)').extract()
            else:
                img = ''
            sel = Selector(response)
            if sel.xpath('//*[@id="article"]//text()'):
                content = ''.join(sel.xpath('//*[@id="article"]//text()').extract()).strip()
            else:
                content = ''
            if response.css('body > div.m.mt15 > div.news_left > div.view > div:nth-child(7) > a::text'):
                lianjie = response.css('body > div.m.mt15 > div.news_left > div.view > div:nth-child(7) > a::text').extract_first()
            # 'body > div.m.mt15 > div.news_left > div.view > div:nth-child(7) > a'
            else:
                lianjie = ''
            daodu = sel.xpath('//meta[@name="description"]/@content').extract()
            if len(daodu) == 0:
                daodu = 'kong'
            else:
                daodu = daodu[0]
            data['daodu']=daodu
            data['title'] = title
            data['data_time'] = data_time
            data['lai'] = lai
            data['authors'] = authors
            data['biaoqian'] = biaoqian
            data['img'] = img
            data['content'] = content
            data['lianjie'] = lianjie
            yield data
        except Exception as e:
            if not os.path.exists('log'):
                os.mkdir('log')
            with open('log.text',encoding='utf-8')as f:
                f.write('{0}'+'\n'+'{1}'.format(e,aurl))



        # print('哈哈哈哈',lai,authors)
        # print(response.url)