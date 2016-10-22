# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.dialects.postgresql import insert
from .models import RaceMeta, RacePayoff, RaceResult, Jockey, create_all_tables
from blacktide.items import RaceResultItem, JockeyItem


class TminazumaPipeline(object):
    def __init__(self, db_conf):
        self.engine = create_engine(URL(**db_conf))
        self.conn = self.engine.connect()
        self.session = sessionmaker(bind=self.engine)()
        create_all_tables(self.engine)

    def insert_race_result(self, item):
        stmt = insert(RaceMeta).values(
            **item['meta']
        ).on_conflict_do_update(
            constraint='race_meta_pkey',
            set_=item['meta']
        )
        self.conn.execute(stmt)
        for x in item['result']:
            stmt = insert(RaceResult).values(
                **x
            ).on_conflict_do_update(
                constraint='race_result_pkey',
                set_=x
            )
            self.conn.execute(stmt)
        for x in item['payoff']:
            stmt = insert(RacePayoff).values(
                **x
            ).on_conflict_do_update(
                constraint='race_payoff_pkey',
                set_=x
            )
            self.conn.execute(stmt)

    def insert_jockey(self, item):
        stmt = insert(Jockey).values(
            **item
        ).on_conflict_do_update(
            constraint='jockeys_pkey',
            set_=dict(item)
        )
        self.conn.execute(stmt)

    def process_item(self, item, spider):
        trans = self.conn.begin()
        spider.logger.debug('start to insert db')
        try:
            if isinstance(item, RaceResultItem):
                self.insert_race_result(item)
            elif isinstance(item, JockeyItem):
                self.insert_jockey(item)
            trans.commit()
        except:
            trans.rollback()
            raise
        spider.logger.debug('done.')

        return item

    @classmethod
    def from_crawler(cls, crawler):
        db_conf = crawler.settings.getdict('SQLALCHEMY_DB_CONF')
        return cls(db_conf)
