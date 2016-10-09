# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RaceResultItem(scrapy.Item):
    meta = scrapy.Field()
    result = scrapy.Field()
    payoff = scrapy.Field()


class HorseItem(scrapy.Item):
    horse_id = scrapy.Field()
    sex_age = scrapy.Field()
    horse_name = scrapy.Field()
    birthday = scrapy.Field()
    color = scrapy.Field()
    trainer = scrapy.Field()
    owner = scrapy.Field()
    producer = scrapy.Field()
    birthplace = scrapy.Field()
    blood = scrapy.Field()
