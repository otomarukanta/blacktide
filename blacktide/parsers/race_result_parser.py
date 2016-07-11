import re
from blacktide.items import RaceResultItem


class RaceResultParser():
    id_regex = re.compile(r'.*?race\/result\/(\d+)')

    def parse(self, res):
        item = RaceResultItem()

        item['race_id'] = self.id_regex.match(res.url).group(1)
        item['race_no'] = res.xpath(
                '//td[@id="raceNo"]/text()').extract_first()

        infos = res.xpath('//div[@id="raceTitName"]/*')
        item['schedule'] = [
                s.strip() for s in infos[0].xpath('text()').extract()]
        item['race_name'] = infos[1].xpath('text()').extract_first().strip()
        item['weather'], item['ground_condition'] = \
            infos[2].xpath('img/@alt').extract()
        info_list = [s.strip('[],\n ')
                     for s in infos[2].xpath('text()').extract()]
        item['distance'] = info_list[0]
        item['qualification'] = info_list[6]
        item['condition'] = info_list[7]
        item['prize'] = info_list[8]

        keys = res.xpath(
                '//div[@class="clearFix"]//th/text()').extract()
        rowspan = res.xpath('//div[@class="clearFix"]//th/@rowspan').extract()
        headers = list()
        for k, v in zip(keys, rowspan):
            for i in range(int(v)):
                headers.append(k)

        values = iter(res.xpath(
            '//div[@class="clearFix"]//td/text()').extract())

        item['payoff'] = [(k, v) for k, v in zip(headers, zip(values, values))]

        tr_list = [line.xpath('td/text()').extract()
                   for line
                   in res.xpath('//table[@id="resultLs"]/.').xpath('tr')]
        item['result'] = [list(map(lambda x: x.strip(), line))
                          for line in tr_list if line]
        return item
