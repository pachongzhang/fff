# -*- coding: utf-8 -*-
import scrapy,re

from newspaper import Article
class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    # allowed_domains = ['www.']
    # start_urls = ['http://www./']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    }

    def start_requests(self):
        global kew
        kew = '萝卜'
        url = 'https://www.baidu.com/s?ie=utf-8&cl=2&rtt=1&bsst=1&tn=news&word='+str(kew)
        yield scrapy.Request(url,callback=self.parse,headers=self.headers)
    def parse(self, response):
        urls = response.xpath("//div/h3[@class='c-title']/a/@href").extract()
        for url in urls:
            # print(url)
            yield scrapy.Request(url,self.detail)
    def detail(self,response):
        new = Article(url=response.url, language='zh')
        new.download()
        new.parse()

        title=new.title

        content=new.text
        # biaoti=new.keywords
        # title = response.xpath("//div[@class='article-title']/h2/text()").extract_first()
        print(new.keywords)