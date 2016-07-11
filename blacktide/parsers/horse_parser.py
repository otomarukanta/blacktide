import re
from blacktide.items import HorseItem


class HorseParser():
    id_regex = re.compile(r'.*?directory\/horse\/(\d+)')

    def parse(self, res):
        item = HorseItem()

        item['horse_id'] = self.id_regex.match(res.url).group(1)

        return item
