# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.spiders.crawl import CrawlSpider,Rule
# from scrapy.linkextractors import LinkExtractor
# import json
# import re
# import os
# from urllib import request
# class SougouSpider(CrawlSpider):
#     name = 'sougou'
#     allowed_domains = []
#     global keyword
#     keyword=input('请输入要听的歌的关键词：')
#     start_urls = ['https://songsearch.kugou.com/song_search_v2?&keyword={}&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0'.format(keyword)]
#     # rules = (
#     #     Rule(LinkExtractor(allow=(r'http://ai.ailab.cn/?.*'),restrict_css=('div.text-c a')),follow=True),
#     #     Rule(LinkExtractor(allow=(r'http://ai.ailab.cn/article-.html'),restrict_css=('ul.list_jc li a')),callback='parse_items',follow=False),
#     # )
#     def parse(self, response):
#         list=re.match('.*?({.*}).*',response.text, re.S).group(1)
#         data= json.loads(list).get('data').get('lists')
#         # print(data)
#         for i in data:
#             # print(i)
#             # p_id = i.get('AlbumID')
#             hase=i.get('FileHash')
#             name=i.get('FileName')
#             html='https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={0}'.format(hase)
#             yield scrapy.Request(html,self.show,meta={'name':name})
#     def show(self, response):
#         data=json.loads(response.text).get('data')
#         if data:
#             url=data.get('play_url')
#             name=data.get('audio_name')
#             # print(name,url)
#             path='./音乐'
#             if url and name:
#                 if os.path.exists(path):
#                     pass
#                 else:
#                     os.makedirs(path)
#                 request.urlretrieve(url,path+'/'+name+'.mp3')
#             # 'https://songsearch.kugou.com/song_search_v2?&keyword='+keyword+'&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0'
#
