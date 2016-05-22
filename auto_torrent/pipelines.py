# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from settings import ALLOWED_SOURCES, MIN_SEEDERS, SIZE_CONSTRAINTS
import re
from mongo import MongoConn



class AutoTorrentPipeline(object):
    def process_item(self, item, spider):
        required_fields = ['magnet_link', 'title', 'source', 'seeders', 'size']
        if all(field in item for field in required_fields):
            return item
        else:
            raise DropItem("Item contains missing fields")

class ScrubbingPipeline(object):
    def process_item(self, item, spider):

        # strip extra whitespace and lower casing
        for key, value in item.items():
            item[key] = value.strip().lower()

        # get item specifics
        seeders = int(item.get('seeders').replace(' ', ''))
        source = item.get('source').strip().lower()
        size_units = item.get('size')[-2:]
        size = int(float(re.search('([0-9.]*)', item.get('size').strip()).group(1)))
        if size_units == 'gb':
            size = size * 1000

        if seeders < MIN_SEEDERS:
            raise DropItem("Item does not meet min seeders")

        if source not in ALLOWED_SOURCES:
            raise DropItem("Item not from allowed source")

        if size not in xrange(SIZE_CONSTRAINTS[0], SIZE_CONSTRAINTS[1]):
            print size, SIZE_CONSTRAINTS
            raise DropItem("Item not within size requirements")

        return item

class MongoDBPipeline(object):
    def process_item(self, item, spider):
        MongoConn().torrents_coll.insert(dict(item))
        log.msg("Torrent added to MongoDB database!", level=log.DEBUG, spider=spider)
        return item