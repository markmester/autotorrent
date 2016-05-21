# -*- coding: utf-8 -*-
# models for scraped items
import scrapy


class PirateItem(scrapy.Item):
    magnet_link = scrapy.Field()
    title = scrapy.Field()
    season = scrapy.Field()
    episode = scrapy.Field()
    seeders = scrapy.Field()
    leechers = scrapy.Field()
    source = scrapy.Field()
    size = scrapy.Field()
    seeders = scrapy.Field()