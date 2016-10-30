# -*- coding: utf-8 -*-
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from blacktide.parsers import RaceResultParser
from blacktide.parsers import HorseParser, JockeyParser


class TminazumaSpider(CrawlSpider):
    name = 'tminazuma'
    allowed_domains = ['keiba.yahoo.co.jp']
    _race_result_parser = RaceResultParser()
    regex_race_result = re.compile(r'/race/result/')

    rules = (
        Rule(LinkExtractor(allow=r'/race/list/')),
        Rule(LinkExtractor(allow=r'/race/result/'),
             follow=True,
             process_links='exclude_race_result',
             callback='parse_result'),
        Rule(LinkExtractor(allow=r'/directory/horse/\d+/\Z'),
             follow=False,
             callback=HorseParser.parse),
        Rule(LinkExtractor(allow=r'/directory/jocky/'),
             follow=False,
             callback=JockeyParser.parse),
    )

    def __init__(self, *args, **kargs):
        super(TminazumaSpider, self).__init__(*args, **kargs)
        self.start_urls = ['http://keiba.yahoo.co.jp/schedule/list/']

    def parse_result(self, response):
        self.logger.debug("parseing ...")
        parsed = self._race_result_parser.parse(response)
        self.logger.debug("done")
        return parsed

    def exclude_race_result(self, links):
        return filter(lambda x: not self.regex_race_result.search(x.url), links)
