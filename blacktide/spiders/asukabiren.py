# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from blacktide.parsers import HorseParser as parser


class AsukaBirenSpider(CrawlSpider):
    name = 'asukabiren'
    allowed_domains = ['keiba.yahoo.co.jp']

    rules = (
        Rule(LinkExtractor(allow=r'/directory/horsesearch/')),
        Rule(LinkExtractor(allow=r'/directory/horse/\d+/\Z'),
             follow=False,
             callback='parse_horse'),
    )

    def __init__(self, *args, **kargs):
        super(AsukaBirenSpider, self).__init__(*args, **kargs)
        self.start_urls = ['http://keiba.yahoo.co.jp/directory/horsesearch/']

    def parse_horse(self, response):
        self.logger.debug("parseing ...")
        parsed = parser.parse(response)
        self.logger.debug("done")
        return parsed
