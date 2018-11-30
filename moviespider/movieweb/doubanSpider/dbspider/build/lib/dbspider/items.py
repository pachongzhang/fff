# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

import sys
# print(sys.path)
sys.path.append('/home/rock/Desktop/moviespider/movieweb/movie')
# import pdb;pdb.set_trace()
# from ....movie.models import Movie, Country, LeadRole, StyleType
from scrapy_djangoitem import DjangoItem
from movie.models import Movie, Country, LeadRole, StyleType

# class DoubanspiderItem(scrapyItem):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class MovieItem(DjangoItem):
    django_model = Movie

class CountryItem(DjangoItem):
    django_model = Country

class LeadRoleItem(DjangoItem):
    django_model = LeadRole

class StyleTypeItem(DjangoItem):
    django_model = StyleType
