import scrapy,re

from newspaper import Article
class RenmingSpider(scrapy.Spider):
    name = 'renmin'
    # allowed_domains = ['www.']
    # start_urls = ['http://www.ttbz.org.cn/']
    headers = {
      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'no-cache',
'Connection': 'keep-alive',
'Cookie': 'JSESSIONID=F546BB1323195E5CF66098DAB40E548B; ALLYESID4=10655888F3FBF143; sso_c=0; sfr=1; _ma_tk=6c6i9v8fqvyprv32klseiqhb5lxufcaz; wdcid=40f43fa4f6e401d5; _people_ip_new_code=100000; _ma_starttm=1543819767511',
'Host':'search.people.com.cn',
'Pragma':'no-cache',
'Referer': 'http://search.people.com.cn/cnpeople/news/getNewsResult.jsp',
'Upgrade-Insecure-Requests': 1,
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36',
    }
    keyword=input('请输入要搜索的内容：')
    page=int(input('请输入页码：'))
    def start_requests(self):
        url='http://search.people.com.cn/cnpeople/search.do?pageNum={0}&keyword={1}&siteName=news&facetFlag=true&nodeType=belongsId&nodeId=0'.format(self.page,self.keyword)
        yield scrapy.Request(url,callback=self.parse)
    def parse(self, response):
        urls = response.xpath('//*[@class="fr w800"]/ul/li[1]/b/a/@href').extract()
        for i in urls:
            # print(i)
            yield scrapy.Request(i,self.detail)
    def detail(self,response):
        title=''.join(response.xpath('//h1//text()').extract()).strip()
        cont=''.join(response.xpath('//*[@class="box_con"]//text()').extract()).strip()
        author=''.join(response.xpath('//*[@class="edit clearfix"]//text()').extract()).strip()
        time=response.xpath('//*[@class="fl"]/text()').extract()
        # new=Article(url=response.url,language='zh')
        # new.download()
        # new.parse()
        # cont=new.text
        # key=new.images
        # time=''.join(response.xpath('//*[@class="listpage_newsbox"]/div/text()').extract()).strip()
        print(title,cont,author)
