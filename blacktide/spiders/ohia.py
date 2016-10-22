# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from blacktide.parsers import JockeyParser as parser


class OhiaSpider(CrawlSpider):
    name = 'ohia'
    allowed_domains = ['keiba.yahoo.co.jp']

    rules = (
        Rule(LinkExtractor(allow=r'/directory/jockeysearch/')),
        Rule(LinkExtractor(allow=r'/directory/jockey/'),
             follow=False,
             callback='parse'),
    )

    def __init__(self, *args, **kargs):
        super(OhiaSpider, self).__init__(*args, **kargs)
        self.start_urls = ['http://keiba.yahoo.co.jp/directory/jockeysearch/']

    def parse(self, response):
        self.logger.debug("parseing ...")
        parsed = parser.parse(response)
        self.logger.debug("done")
        return parsed
