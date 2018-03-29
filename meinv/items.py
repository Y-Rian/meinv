# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeinvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    album_url = scrapy.Field()
    album_title = scrapy.Field()
    image_title = scrapy.Field()
    image_url = scrapy.Field()
    album_count = scrapy.Field()
    tag = scrapy.Field()