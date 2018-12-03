import scrapy,re

from newspaper import Article
class FangSpider(scrapy.Spider):
    name = 'fang'
    # allowed_domains = ['www.']
    start_urls = ['http://zu.fang.com/house/a21/']
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36'
    }
    def parse(self, response):
        urls = response.xpath('//*[@class="title"]/a[1]/@href').extract()
        for i in urls:
            url='http://www.ttbz.org.cn/'+i
            yield scrapy.Request(url,self.detail)
    def detail(self,response):
        title = response.xpath('//div[5]/div[1]/h1/text()')[0]  # 抓取标题
        address = response.xpath( '//div[5]/div[1]/div[2]/div[5]/div[3]/div[2]/a/text()|/html/body/div[5]/div[1]/div[2]/div[5]/div[2]/div[2]/a/text()')[0]
        price = response.xpath('//div[5]/div[1]/div[2]/div[2]/div/i/text()')[0]
        time_str = response.xpath('//div[5]/div[1]/p/span[2]/text()')[0]
        text =response.xpath('//div[5]/div[2]/div[1]/div[1]/div[2]/p/text()')[0]
