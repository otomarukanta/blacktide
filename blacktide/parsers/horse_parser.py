import re
from datetime import date
from blacktide.items import HorseItem


number_regex = re.compile(r'\d+')


def parse(res):
    item = HorseItem()

    item['horse_id'] = number_regex.search(res.url).group()
    for x in res.xpath('//div[@id="dirTitName"]/p/text()').extract():
        if x.strip() in ['牡', '牡', 'せん']:
            item['sex'] = x.strip()
            break
    else:
        return item
    item['horse_name'] = res.xpath(
            '//div[@id="dirTitName"]/h1/text()').extract_first()
    birthday, item['color'], _, \
        item['owner'], item['producer'], item['birthplace'] = [
            x.xpath('text()').extract_first()
            for x in res.xpath('//div[@id="dirTitName"]/ul/li/.')]
    item['trainer_id'] = number_regex.search(res.xpath(
        '//div[@id="dirTitName"]/ul/li/a/@href').extract_first()).group()
    item['birthday'] = date(*map(int, number_regex.findall(birthday)))

    item['sire'], item['sire_sire'], item['sire_sire_sire'], \
        item['sire_sire_mare'], item['sire_mare'], \
        item['sire_mare_sire'], item['sire_mare_mare'], \
        item['mare'], item['mare_sire'], item['mare_sire_sire'], \
        item['mare_sire_mare'], item['mare_mare'], \
        item['mare_mare_sire'], item['mare_mare_mare'] = \
        [x.xpath('text()').extract_first()
         for x in res.xpath('//table[@id="dirUmaBlood"]/*/td/.')]

    return item
