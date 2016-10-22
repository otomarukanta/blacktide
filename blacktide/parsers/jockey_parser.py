import re
from blacktide.items import JockeyItem

number_regex = re.compile(r'\d+')


def parse(res):
    item = JockeyItem()

    item['jockey_id'] = number_regex.search(res.url).group()
    item['name'] = res.xpath(
            '//div[@id="dirTitName"]/p/text()').extract_first().strip()
    item['kana'] = res.xpath(
            '//div[@id="dirTitName"]/h1/text()').extract_first().strip()

    return item
