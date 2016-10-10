# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from .models import RaceMeta, RacePayoff, RaceResult, create_all_tables


class TminazumaPipeline(object):
    def __init__(self, db_conf):
        self.engine = create_engine(URL(**db_conf))
        self.session = sessionmaker(bind=self.engine)()
        create_all_tables(self.engine)

    def process_item(self, item, spider):
        try:
            self.session.merge(RaceMeta(**item['meta']))
            [self.session.merge(RaceResult(**x)) for x in item['result']]
            [self.session.merge(RacePayoff(**x)) for x in item['payoff']]
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
        return item

    @classmethod
    def from_crawler(cls, crawler):
        db_conf = crawler.settings.getdict('SQLALCHEMY_DB_CONF')
        return cls(db_conf)
