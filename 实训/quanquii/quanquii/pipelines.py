# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
my_client=pymongo.MongoClient()['wu']['renjiN']
class QuanquiiPipeline(object):
    def process_item(self, item, spider):
        my_client.save(dict(item))
        return item
