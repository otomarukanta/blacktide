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

    def __repr__(self):
        return repr({"meta": self['meta']})


class JockeyItem(scrapy.Item):
    jockey_id = scrapy.Field()
    name = scrapy.Field()
    kana = scrapy.Field()


class HorseItem(scrapy.Item):
    horse_id = scrapy.Field()
    sex = scrapy.Field()
    horse_name = scrapy.Field()
    birthday = scrapy.Field()
    color = scrapy.Field()
    trainer_id = scrapy.Field()
    owner = scrapy.Field()
    producer = scrapy.Field()
    birthplace = scrapy.Field()
    sire = scrapy.Field()
    sire_sire = scrapy.Field()
    sire_sire_sire = scrapy.Field()
    sire_sire_mare = scrapy.Field()
    sire_mare = scrapy.Field()
    sire_mare_sire = scrapy.Field()
    sire_mare_mare = scrapy.Field()
    mare = scrapy.Field()
    mare_sire = scrapy.Field()
    mare_sire_sire = scrapy.Field()
    mare_sire_mare = scrapy.Field()
    mare_mare = scrapy.Field()
    mare_mare_sire = scrapy.Field()
    mare_mare_mare = scrapy.Field()
