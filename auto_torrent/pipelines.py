# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import re



class AutoTorrentPipeline(object):
    def process_item(self, item, spider):
        required_fields = ['magnet_link', 'title']
        if all(field in item for field in required_fields):
            return item
        else:
            raise DropItem("Item contains missing fields")

class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Torrent added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
