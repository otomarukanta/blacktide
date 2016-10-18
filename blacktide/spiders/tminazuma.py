# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from blacktide.parsers import RaceResultParser


class TminazumaSpider(CrawlSpider):
    name = 'tminazuma'
    allowed_domains = ['keiba.yahoo.co.jp']
    _race_result_parser = RaceResultParser()

    rules = (
        Rule(LinkExtractor(allow=r'/race/list/')),
        Rule(LinkExtractor(allow=r'/race/result/'),
             follow=False,
             callback='parse_result'),
    )

    def __init__(self, *args, **kargs):
        super(TminazumaSpider, self).__init__(*args, **kargs)
        self.start_urls = ['http://keiba.yahoo.co.jp/schedule/list/']

    def parse_result(self, response):
        self.logger.debug("parseing ...")
        parsed = self._race_result_parser.parse(response)
        self.logger.debug("done")
        return parsed
