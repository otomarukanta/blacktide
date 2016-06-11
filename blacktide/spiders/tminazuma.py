# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from blacktide.items import BlacktideItem


class TminazumaSpider(CrawlSpider):
    name = 'tminazuma'
    allowed_domains = ['keiba.yahoo.co.jp']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def __init__(self, year, month, *args, **kargs):
        super(TminazumaSpider, self).__init__(*args, **kargs)
        self.start_urls = [
            'http://keiba.yahoo.co.jp/schedule/list/{}/?month={}'
            .format(year, month)
            ]

    def parse_item(self, response):
        i = BlacktideItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
