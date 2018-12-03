import scrapy,re

from newspaper import Article
class AnjuSpider(scrapy.Spider):
    name = 'anju'
    # allowed_domains = ['www.']
    start_urls = ['https://beijing.anjuke.com/sale/']
    # headers = {
    #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36'
    # }
    def parse(self, response):
        # print(response.text)
        urls = response.xpath('//*[@class="house-title"]/a[1]/@href').extract()
        for i in urls:
            # print(i)
            yield scrapy.Request(i,self.detail)
    def detail(self,response):
        # print(response.url)
        new=Article(url=response.url,language='zh')
        new.download()
        new.parse()
        title=new.title
        price=response.xpath('//*[@class="clearfix"]/div/span[1]/em/text()').extract()
        print(new.text,price)
