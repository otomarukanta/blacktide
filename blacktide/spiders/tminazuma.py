# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from blacktide.parsers import RaceResultParser, HorseParser


class TminazumaSpider(CrawlSpider):
    name = 'tminazuma'
    allowed_domains = ['keiba.yahoo.co.jp']
    _race_result_parser = RaceResultParser()
    _horse_parser = HorseParser()

    rules = (
        Rule(LinkExtractor(allow=r'/race/list/'),
             follow=True, callback='parse_list'),
        Rule(LinkExtractor(allow=r'/race/result/'),
             follow=True, callback='parse_result'),
        Rule(LinkExtractor(allow=r'/directory/horse/\d+?/\Z'),
             follow=False, callback='parse_horse'),
        Rule(LinkExtractor(allow=r'/directory/jocky/\d+?/\Z'),
             follow=False, callback='parse_jockey'),
        Rule(LinkExtractor(allow=r'/directory/trainer/\d+?/\Z'),
             follow=False, callback='parse_trainer'),
    )

    def __init__(self, year, month, *args, **kargs):
        super(TminazumaSpider, self).__init__(*args, **kargs)
        self.start_urls = [
            'http://keiba.yahoo.co.jp/schedule/list/{}/?month={}'
            .format(year, month)
            ]

    def parse_result(self, response):
        return self._race_result_parser.parse(response)

    def parse_horse(self, response):
        return self._horse_parser.parse(response)
