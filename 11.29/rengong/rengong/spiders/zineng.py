# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import io,sys
from scrapy.spiders import Spider
# reload(sys)sys.setdefaultencoding('utf-8')
class ZinengSpider(CrawlSpider):
    name = 'zineng'
    allowed_domains = []
    # start_urls = ['http://ai.ailab.cn']
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36',
        'Cookie':'nRhl_ba1e_saltkey=H1C1C7q7; nRhl_ba1e_lastvisit=1543487912; UM_distinctid=1675f43764a223-0a14e1e4e6d18e-675d7620-1fa400-1675f43764c3b4; Hm_lvt_7727b26d56bdd09333b33d957ec500a9=1543492013; nRhl_ba1e_lastrequest=941byVQMFm%2FocBwxFsTp7YiI3O1Hp%2FxGern4ECHDwZlhsnTo6TUD; CNZZDATA3202821=cnzz_eid%3D237531997-1543486415-null%26ntime%3D1543649616; nRhl_ba1e_lastact=1543651634%09index.php%09',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }
    default = True

    def start_requests(self):
        for i in range(1, 5):
            url = 'http://www.ailab.cn/?page=' + str(i)
            yield scrapy.Request(url)

    def parse(self, response):
        # sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
        if self.date==True:
            url=response.url
            self.date=False
            yield scrapy.Request(url,self.parse,headers=self.header)
        else:
            # print(response.text)
            d_url=response.css('ul.list_jc li > a ::attr(href)').extract()
            for i in d_url:
                yield scrapy.Request(i,self.parse1,headers=self.header)
            page=response.css('div.pg strong ::text').extract_first()
            # if response.css('a.last::text'):
            #     next_url='http://www.ailab.cn/?page='+str(int(page)+1)
            #     yield scrapy.Request(next_url,self.parse,headers=self.header)
            #     self.date=True
            # else:
            #     print('没有下一页了')

            # print(page,d_url)
    def parse1(self, response):
        try:
            if response.css('h1.h1 ::text'):
                title=response.css('.h1.h1 ::text').extract_first()
            else:
                raise Exception('title is None')
            if response.css('div.p::text'):
                data_time=response.css('div.p ::text').re('\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
            else:
                data_time=''
            if response.css('meta[name="description"] ::attr(content)'):
                daodu=response.css('meta[name="description"] ::attr(content)').extract()
            else:
                daodu=''
            if response.css('div.tag a::text'):
                biaoqian=response.css('div.tag a::text').extract()
            else:
                biaoqian = ''
            print(response.url,title, data_time)
        except Exception as e:
            pass

