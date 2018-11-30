#coding;utf-8
import scrapy
import time
from urllib import parse

class MovieSpider(scrapy.Spider):
    name = 'movie'  # 爬虫名
    # allowed_domains = ['movie.douban.com']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    page = 1  # 翻页记录
    url = 'https://movie.douban.com/top250'

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers)

    # 解析页面
    def parse(self, response):
        # item = DoubanmovieItem()
        movie_ol = response.xpath('//ol[@class="grid_view"]/li/div/div[2]')

        for div in movie_ol:
            # 电影名称和评分
            item = {}
            name = div.xpath('.//a/span[1]/text()').extract_first()
            mark = div.xpath('.//span[@class="rating_num"]/text()').extract_first()
            temp = response.xpath('//div[starts-with(@class,"bd")]/p/text()[2]').extract_first()

            item = {
                'name':name,
                'mark':mark,
                'release_time':str(temp).split('/')[0].strip(),
            }

            country = str(temp).split('/')[1].strip()
            if '韩国' in country:
                item['country'] = 1
            elif '美国' in country or ('英国' in country):
                item['country'] = 2
            elif '中国' in country:
                item['country'] = 3
            elif '日本' in country:
                item['country'] = 4
            else:
                item['country'] = 5

            # 电影详情信息页面url
            detail_url = div.xpath('.//a/@href').extract_first()

            # 获取详细信息
            yield scrapy.Request(url=detail_url, callback=self.parse_info, meta={'item':item}, dont_filter=True)


        # 翻页
        if self.page <= 9:
            data = {
                'start':(self.page ) * 25,
            }
            data = parse.urlencode(data)

            # 下一页url
            next_url = 'https://movie.douban.com/top250?' + data
            self.page += 1

            yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)

    # 解析每一条电影链接对应的详情页信息
    def parse_info(self, response):
        item = response.meta['item']

        director = response.xpath('//div[@class="article"]//div[@id="info"]/span[1]/span[2]/a/text()').extract_first()
        type1 = response.xpath('//div[@class="article"]//div[@id="info"]/span[5]/text()').extract_first()
        type2 = response.xpath('//div[@class="article"]//div[@id="info"]/span[6]/text()').extract_first()
        # role1 = response.xpath('//div[@class="article"]//div[@id="info"]/span[3]/span[2]/span[1]/a/text()').extract_first()
        # role2 = response.xpath(
        #     '//div[@class="article"]//div[@id="info"]/span[3]/span[2]/span[2]/a/text()').extract_first()
        length = response.xpath('//div[@class="article"]//div[@id="info"]/span[@class="pl"][5]/following-sibling::span[1]/text()').extract_first()
        imdb_link = response.xpath('//div[@class="article"]//div[@id="info"]/a[1]/@href').extract_first()
        cover_link = response.xpath('//div[@class="article"]//div[@id="mainpic"]//img/@src').extract_first()
        summary = response.xpath('//div[@class="article"]//div[@id="link-report"]/span[1]/span/text()[1]').extract_first()

        if summary == None:
            summary = response.xpath('//div[@class="article"]//div[@id="link-report"]/span[1]/text()[1]').extract_first()

        item['director'] = director
        item['length'] = length[0:3]
        item['imdb_link'] = imdb_link
        item['cover_link'] = cover_link
        item['summary'] = summary.strip()
        # item['role1'] = role1
        item['type1'] = type1
        # item['role2'] = role2
        item['type2'] = type2



        time.sleep(2)
        yield item