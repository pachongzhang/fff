# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuanquiiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    data_time = scrapy.Field()
    name = scrapy.Field()
    lai = scrapy.Field()
    authors = scrapy.Field()
    biaoqian = scrapy.Field()
    img = scrapy.Field()
    content = scrapy.Field()
    lianjie = scrapy.Field()
    daodu = scrapy.Field()
    # img = scrapy.Field()
    pass
