# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.dialects.postgresql import insert
from .models import RaceMeta, RacePayoff, RaceResult, create_all_tables


class TminazumaPipeline(object):
    def __init__(self, db_conf):
        self.engine = create_engine(URL(**db_conf))
        self.conn = self.engine.connect()
        self.session = sessionmaker(bind=self.engine)()
        create_all_tables(self.engine)

    def process_item(self, item, spider):
        spider.logger.debug('start to insert db')
        trans = self.conn.begin()
        try:
            stmt = insert(RaceMeta).values(
                **item['meta']
            ).on_conflict_do_update(
                constraint='race_meta_pkey',
                set_=dict(race_id=item['meta']['race_id'])
            )
            self.conn.execute(stmt)
            for x in item['result']:
                stmt = insert(RaceResult).values(
                    **x
                ).on_conflict_do_update(
                    constraint='race_result_pkey',
                    set_=dict(race_id=x['race_id'], row=x['row'])
                )
                self.conn.execute(stmt)
            for x in item['payoff']:
                stmt = insert(RacePayoff).values(
                    **x
                ).on_conflict_do_update(
                    constraint='race_payoff_pkey',
                    set_=dict(race_id=x['race_id'], odds_id=x['odds_id'])
                )
                self.conn.execute(stmt)
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
