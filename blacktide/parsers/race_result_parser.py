import re
from collections import defaultdict
from datetime import datetime
from blacktide.items import RaceResultItem


class RaceResultParser():
    id_regex = re.compile(r'.*?race\/result\/(\d+)')
    date_regex = re.compile(r'(\d+)年(\d+)月(\d+)日')
    number_regex = re.compile(r'\d+')
    grade_regex = re.compile(r"\d+?万下|オープン|新馬|未勝利|未出走")

    surface_set = set(['芝', 'ダート', '芝→ダート'])
    rotation_set = set(['右', '左', '直線'])
    side_set = set(['内', '外', '内->外', '外->内', '外→内', '内2周', '外2周'])

    def parse(self, res):
        item = RaceResultItem()
        self.race_id = self.id_regex.match(res.url).group(1)
        item['meta'] = self.__parse_meta(res)
        item['result'] = self.__parse_result(res)
        item['payoff'] = self.__parse_payoff(res)

        return item

    def __parse_meta(self, res):
        ret = dict()
        ret['race_id'] = self.race_id
        ret['race_name'] = res.xpath('//h1[@class="fntB"]/text()')\
                              .extract_first().strip()
        ret['race_no'] = self.number_regex.findall(
                res.xpath('//td[@id="raceNo"]/text()').extract_first())[0]

        date, place, time = res.xpath('//p[@id="raceTitDay"]/text()').extract()
        year, month, day = self.number_regex.findall(date)
        hour, mins = self.number_regex.findall(time)
        ret['race_datetime'] = datetime(int(year), int(month), int(day),
                                        int(hour), int(mins))
        ret['race_days'], ret['race_weeks'] = self.number_regex.findall(place)

        metas = res.xpath('//p[@id="raceTitMeta"]/text()').extract()
        ret['race_grade'] = self.__get_race_grade(ret['race_name'], metas[7])

        ret['track_weather'], ret['track_condition'] = \
            res.xpath('//p[@id="raceTitMeta"]/img/@alt').extract()
        ret['track_meter'] = self.number_regex.findall(metas[0])[0]
        ret['track_place'] = res.xpath('//li[@id="racePlaceNaviC"]/a/text()')\
                                .extract_first()
        track_set = set(metas[0].split(' ')[0].split('・'))
        ret['track_surface'] = self.__get_matched(self.surface_set, track_set)
        ret['track_side'] = self.__get_matched(self.side_set, track_set)
        ret['track_type'] = self.__get_track_type(track_set)
        ret['track_rotation'] = self.__get_matched(
                self.rotation_set, track_set)

        conditions = self.__get_conditions(metas[7])
        ret['cond_intl'] = conditions['international']
        ret['cond_jockey'] = conditions['jockey']
        ret['cond_local'] = conditions['local']
        ret['cond_weight'] = conditions['weight']
        ret['cond_age'] = metas[6].strip()

        ret['prize1'], ret['prize2'], ret['prize3'], ret['prize4'],\
            ret['prize5'] = metas[8].strip(' 本賞金：万円').split('、')

        return ret

    def __parse_result(self, res):
        ret = list()

        tr_list = [x.xpath('td')
                   for x
                   in res.xpath('//table[@id="resultLs"]/.').xpath('tr')
                   if x.xpath('td')]

        for i, x in enumerate(tr_list):
            line = dict()
            line['race_id'] = self.race_id
            line['row'] = i
            line['fp'] = self.__get_text(x[0])
            line['bk'] = x[1].xpath('span/text()')[0].extract().strip()
            line['pp'] = self.__get_text(x[2])
            line['horse_id'] = self.__get_id(x[3])
            sex_age = self.__get_text(x[4])
            line['horse_sex'] = sex_age.strip('1234567890')
            line['horse_age'] = sex_age.strip(line['horse_sex'])
            line['jockey_id'] = self.__get_id(x[5])
            try:
                line['time'] = self.__parse_time(self.__get_text(x[6]))
            except:
                line['time'] = None
            line['margin'] = self.__get_text(x[7])
            try:
                pos = [int(x) for x in self.__get_text(x[8]).split('-')]
            except:
                pos = list()
            line['first_position'] = pos[-4] if len(pos) > 3 else None
            line['second_position'] = pos[-3] if len(pos) > 2 else None
            line['third_position'] = pos[-2] if len(pos) > 1 else None
            line['fourth_position'] = pos[-1] if len(pos) > 0 else None
            line['l3f'] = self.__parse_time(self.__get_text(x[9]))
            line['jockey_weight'] = float('.'.join(
                self.number_regex.findall(self.__get_text(x[10]))))
            try:
                line['horse_weight'] = self.__get_text(x[11])
            except:
                line['horse_weight'] = None

            try:
                line['fav'] = self.__get_text(x[12])
            except:
                line['fav'] = None

            try:
                line['odds'] = float(self.__get_text(x[13]))
            except:
                line['odds'] = None

            line['blinker'] = self.__get_text(x[14])
            line['trainer_id'] = self.__get_id(x[15])

            ret.append(line)

        return ret

    def __parse_payoff(self, res):
        keys = res.xpath('//div[@class="clearFix"]//th/text()').extract()
        rowspan = res.xpath('//div[@class="clearFix"]//th/@rowspan').extract()
        kinds = list()
        for k, v in zip(keys, rowspan):
            for i in range(int(v)):
                kinds.append(k)

        ret = list()

        for i, tr in enumerate(res.xpath('//div[@class="clearFix"]//tr')):
            line = dict()
            line['race_id'] = self.race_id
            line['odds_id'] = i
            line['kind'] = kinds[i]
            combs, yen, _ = [x.xpath('text()').extract_first()
                          for x in tr.xpath('td')]
            if combs:
                combs = self.number_regex.findall(combs)
            else:
                combs = list()
            line['comb1'] = combs[0] if len(combs) > 0 else None
            line['comb2'] = combs[1] if len(combs) > 1 else None
            line['comb3'] = combs[2] if len(combs) > 2 else None

            yen = self.number_regex.findall(yen)
            line['yen'] = yen[0] if yen else None

            popularity = self.number_regex.findall(
                    tr.xpath('td/span/text()').extract_first())
            if popularity:
                line['popularity'] = popularity[0]
            else:
                line['popularity'] = None
            ret.append(line)

        return ret

    def __get_race_grade(self, name, race_type):
        for grade in ['GIII', 'GII', 'GI']:
            if grade in name:
                return grade
            return self.grade_regex.findall(race_type)[0]

    def __get_track_type(self, track_infos):
        if '障害' in track_infos:
            return '障害'
        else:
            return '平地'

    def __get_matched(self, label_set, target_set):
        matched = label_set.intersection(target_set)
        if len(matched) == 0:
            return None
        elif len(matched) == 1:
            return matched.pop()
        else:
            return None

    def __get_conditions(self, race_conditions):
        condition = defaultdict(lambda: False)

        condition['local'] = list(filter(
            lambda x: x in race_conditions, ['特指', '（指定）', '[指定]']))
        condition['international'] = list(filter(
            lambda x: x in race_conditions, ['国際', '混合', '父', '九州']))
        condition['weight'] = list(filter(
            lambda x: x in race_conditions, ['定量', '別定', 'ハンデ', '馬齢']))
        condition['jockey'] = list(filter(
            lambda x: x in race_conditions, ['']))

        for k, v in condition.items():
            if not v:
                condition[k] = None
            else:
                condition[k] = v[0].strip('（）')

        return condition

    def __parse_time(self, raw):
        if raw == "0." or raw == "99.9":
            t = None
        elif raw.count('.') == 1:
            t = datetime.strptime(raw, '%S.%f').time()
        elif raw.count('.') == 2:
            t = datetime.strptime(raw, '%M.%S.%f').time()
        else:
            t = None
        return t

    def __get_text(self, x):
        a = x.xpath('text()').extract()
        if not a:
            return None
        else:
            return a[0].strip()

    def __get_id(self, x):
        return x.xpath('a/@href')[0].extract().split('/')[3]
