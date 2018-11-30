# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
sys.path.append('/home/rock/Desktop/moviespider/movieweb/movie')

from .items import MovieItem
from movie.models import StyleType, LeadRole, Movie, Country

class DoubanspiderPipeline(object):
    def process_item(self, item, spider):
        movie = MovieItem()
        # rolelist = [item['role1'],item['role2']]
        # for i in rolelist:
        #     LeadRole.objects.get_or_create(name=i)

        typelist = [item['type1'], item['type2']]
        for i in typelist:
            StyleType.objects.get_or_create(style_type=i)

        movie['name'] = item['name']
        movie['mark'] = item['mark']
        movie['release_time'] = item['release_time']
        movie['country'] = Country.objects.get(id=item['country'])
        movie['director'] = item['director']
        movie['length'] = item['length']
        movie['imdb_link'] = item['imdb_link']
        movie['cover_link'] = item['cover_link']
        movie['summary'] = item['summary']

        movie.save()

        m = Movie.objects.get(name = item['name'])
        # m.lead_role.add(LeadRole.objects.get(name=item['role1']))
        # m.lead_role.add(LeadRole.objects.get(name=item['role2']))
        m.style_type.add(StyleType.objects.get(style_type=item['type1']))
        m.style_type.add(StyleType.objects.get(style_type=item['type2']))


        return item
