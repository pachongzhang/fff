import scrapy,re

from newspaper import Article
class TuantiSpider(scrapy.Spider):
    name = 'tuanti'
    # allowed_domains = ['www.']
    start_urls = ['http://www.ttbz.org.cn/']
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36'
    }
    def parse(self, response):
        urls = response.xpath('//*[@id="newArea1"]/ul/li/a/@href').extract()
        for i in urls:
            url='http://www.ttbz.org.cn/'+i
            yield scrapy.Request(url,self.detail)
    def detail(self,response):

            new=Article(url=response.url,language='zh')
            new.download()
            new.parse()
            title=new.text
            key=new.images
            time=''.join(response.xpath('//*[@class="listpage_newsbox"]/div/text()').extract()).strip()
            print(time)
