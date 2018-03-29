# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
import os
from scrapy.pipelines.images import ImagesPipeline

class MeinvPipeline(object):
    def process_item(self, item, spider):
        return item

class SaveImage(ImagesPipeline):
    def get_media_requests(self, item, info):
        pass
    def item_completed(self, results, item, info):
        pass
    def file_path(self, request, response=None, info=None):
        pass


class MongodbPipeline(object):
    # def __init__(self):
    #     db_name = 'xiaojiejie'
    #     collection_name = '55156.com'
    #     self.client = pymongo.MongoClient(host='localhost', port=27017)
    #     self.db = self.client[db_name]
    #     self.post = self.db[collection_name]

    def __init__(self):
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        db_name = settings['MONGO_DB']
        collection_name = settings['MONGO_COLLECTION']
        client = pymongo.MongoClient(host=host,port=port)
        db = client[db_name]
        self.post = db[collection_name]


    def process_item(self,item,spider):

        # data = dict(item)
        data = {
            'album_title': item['album_title'],
            'album_url': item['album_url'],
            'image_title': item['image_title'],
            'imaget_url': item['image_url'],
            'tag': item['tag']
        }
        self.post.insert_one(data)
        print('%s  写入mongodb成功' % item['image_title'])
        return item

