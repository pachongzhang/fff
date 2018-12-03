# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders.crawl import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
import json
import time
from scrapy.selector import Selector
class XinlangSpider(scrapy.Spider):
    name = 'xinlang'
    # allowed_domains = ['cre.mix.sina.com.cn']
    start_urls = ['https://tech.sina.com.cn/']
    cookies={'vjlast': '1541129407', 'SINAGLOBAL': '114.249.232.244_1541129408.485601', 'Apache': '172.16.7.96_1543535404.322739', 'SUBP': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5Tw1EZVhNYzRhZjVc_R2zY', 'vjuids': '62cfb576c.166d2788952.0.d99dbd6227d4a', 'U_TRS1': '000000f5.4111e41.5bdbc4c0.fef9d8b3', 'UOR': ',tech.sina.com.cn,', 'lxlrttp': '1541383354', 'TUIJIAN_1': 'usrmdinst_2', 'ULV': '1543535635000:6:6:2:172.16.7.96_1543535404.322739:1543535401886', 'SUB': '_2AkMsmkoef8NxqwJRmfkXzmnra4hyyA_EieKaxrvFJRMyHRl-yD9jqnY_tRB6Bxpk8UGJfRvB2xXb6yY0pa-Z97pyKAHU', 'hqEtagMode': '1', 'reco': 'usrmdinst_6'}

    def parse(self, response):

        time.sleep(2)
        t_time=str(time.time())[:-8]

        url='https://cre.mix.sina.com.cn/api/v3/get?cateid=1z&cre=tianyi&mod=pctech&'+t_time
        #url='https://cre.mix.sina.com.cn/api/v3/get?&cateid=1z&cre=tianyi&mod=pctech&top_id=%2CA1u1J%2CA1rkN%2CA1s5b%2CA1mJl%2CA1PbX%2CA1MSP%2CA1fbh%2CA1Rzi%2CA1MWO%2CA1MEd%2C%2C9Eux1%2C%2C&ctime=1543456689'
        #print(url)
        yield scrapy.Request(url,callback=self.parse1,cookies=self.cookies)
    def parse1(self,response):
        data=json.loads(response.text).get('data')
        for i in data:
            d_url=i.get('url')
            c_time=i.get('ctime')
            yield scrapy.Request(d_url,self.show)
        if data[-1].get('ctime'):
            ctime = data[-1].get('ctime')
            url = 'https://cre.mix.sina.com.cn/api/v3/get?cateid=1z&cre=tianyi&mod=pctech&ctime=' + str(ctime)
            # print(url)
            yield scrapy.Request(url, callback=self.parse1)
        
    def show(self, response):
        import re
        sel=Selector(response)
        # rea = re.findall("<title>(.*?)</title>",response.text,re.S)
        # print(rea,response.url)

        # try:
        if sel.xpath('//*[@class="main-title"]'):
            title=sel.xpath('//*[@class="main-title"]/text()').extract_first()
        else:
            title = ''
        if sel.xpath('//*[@id="top_bar"]/div/div[2]/span[1]/text()'):
            time=sel.xpath('//*[@id="top_bar"]/div/div[2]/span[1]/text()').extract_first()
        else:
            time=''
        if sel.xpath('//*[@name="keywords"]'):
            biaoqian=sel.xpath('//*[@name="keywords"]/@content').extract_first()
        else:
            biaoqian=''
        if sel.xpath('//*[@class="article-content clearfix"]'):
            author=''.join(sel.xpath('//*[@class="article-content clearfix"]//text()').extract()).strip().replace(' ','')
        else:
            author=''
        print(title,'sjignlkf',time,biaoqian)
        # except Exception as e:
        #     pass
        # print(response.url)
        
        
        