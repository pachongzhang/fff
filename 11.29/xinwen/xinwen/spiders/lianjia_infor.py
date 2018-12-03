# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from bs4 import BeautifulSoup
# from ..items import LianjiaItem

class LianjiaInforSpider(scrapy.Spider):
    name = "lianjia_infor"
    # allowed_domains = ["www.lianjia.com"]
    start_urls = ['https://bj.lianjia.com/ershoufang/']
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36',
        'Cookie':'TY_SESSION_ID=aa1f4fe7-e69e-4c88-8feb-6dde14df5ed5; lianjia_uuid=dcb1682d-5ce4-4aac-b46d-8ec78d1b78c1; UM_distinctid=167152d0666282-070f58cce9051c-675d7620-144000-167152d066737f; _ga=GA1.2.1888059791.1542248536; _smt_uid=5becd877.33a4bca5; select_city=110000; all-lj=8e5e63e6fe0f3d027511a4242126e9cc; CNZZDATA1253477573=283902778-1542243816-%7C1543755140; CNZZDATA1254525948=1022926835-1542244943-%7C1543754199; CNZZDATA1255633284=2099559829-1542247685-%7C1543752219; CNZZDATA1255604082=1253468648-1542244970-%7C1543753532; _jzqa=1.308419838298065800.1542248532.1542256280.1543755430.4; _jzqc=1; _jzqckmp=1; _qzjc=1; _gid=GA1.2.1264556053.1543755436; introduce=1; ljref=pc_sem_baidu_ppzq_x; TY_SESSION_ID=42fd40d7-681c-43d6-b95f-35f9d6641fe8; _jzqy=1.1543755430.1543756507.2.jzqsr=baidu|jzqct=l%E9%93%BE%E5%AE%B6.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1542248530,1543755428,1543756509; lianjia_ssid=6b6b09a0-45d7-4051-b70a-252696da5e19; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1543756517; _qzja=1.1700467799.1542248532583.1542256280151.1543755429692.1543756507443.1543756517429.0.0.0.20.4; _qzjb=1.1543755429692.6.0.0.0; _qzjto=6.1.0; _jzqb=1.6.10.1543755430.1'
    }
    def start_requests(self):
        url_base = 'https://bj.lianjia.com/ershoufang'
        for i in range(1,51):
            url = url_base + '/pg' + str(i) + '/'
            yield scrapy.Request(url,self.parse,headers=self.header)

    def parse(self, response):
        print(response.text)
        item_list = response.xpath('//li[@class="clear LOGCLICKDATA"]')
        for item in item_list:

            title = item.xpath('div/div[1]/a/text()').extract_first()
            # title = item.find('div',attrs={'class':"title"}).find('a').get_text()

            house_infor = ','.join(item.xpath('div/div[2]/div/text()').extract())
            # print(house_infor)
            positionInfo = ','.join(item.xpath('div/div[3]/div/text()|div/div[3]/div/a/text()').extract())
            # print(positionInfo)
            followInfo = ','.join(item.xpath('div/div[4]/text()').extract())
            # print(followInfo)
            subwayInfo = item.xpath('div/div[4]/div[1]/span[@class="subway"]/text()').extract_first()
            # print(subwayInfo)
            taxInfo = item.xpath('div/div[4]/div[1]/span[@class="taxfree"]/text()').extract_first()
            # print(taxInfo)
            haskeyInfo = item.xpath('div/div[4]/div[1]/span[@class="haskey"]/text()').extract_first()
            # print(haskeyInfo)
            totalPrice = item.xpath('div/div[4]/div[2]/div[1]/span/text()').extract_first() + '万'
            # print(totalPrice)
            unitPrice = item.xpath('div/div[4]/div[2]/div[2]/span/text()').extract_first()
            print(house_infor)            # print(unitPrice)
