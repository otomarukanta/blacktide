import re
from blacktide.items import HorseItem


class HorseParser():
    id_regex = re.compile(r'.*?directory\/horse\/(\d+)')

    def parse(self, res):
        item = HorseItem()

        item['horse_id'] = self.id_regex.match(res.url).group(1)
        item['sex_age'] = res.xpath(
                '//div[@id="dirTitName"]/p/text()').extract()
        item['horse_name'] = res.xpath(
                '//div[@id="dirTitName"]/h1/text()').extract_first()
        item['birthday'], item['color'], item['trainer'], \
            item['owner'], item['producer'], item['birthplace'] = res.xpath(
                '//div[@id="dirTitName"]/ul/li/text()').extract()

        item['blood'] = res.xpath(
            '//table[@id="dirUmaBlood"]/*/td/text()').extract()

        return item
