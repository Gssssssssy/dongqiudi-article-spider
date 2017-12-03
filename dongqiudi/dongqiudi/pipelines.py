# -*- coding: utf-8 -*-

import datetime
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys

from scrapy.exceptions import DropItem

from .models import DBSession, Articles

reload(sys)
sys.setdefaultencoding('utf-8')


class DongQiuDiPipeline(object):
    def __init__(self):
        self.session = DBSession()
        self.article_id_seen = set(map(lambda x: int(x[0]), self.session.query(Articles.article_id).all()))
        self.results = []

    def process_item(self, item, spider):
        nt = datetime.datetime.now()
        if item['article_id'] in self.article_id_seen:  # 除重
            raise DropItem("Duplicate item found: %s" % item)
        else:
            art = Articles(created_time=nt, last_updated=nt, **item)
            self.results.append(art)
        self.article_id_seen.add(item['article_id'])

        if item['published_at']:  # 投毒处理
            published_at_2_datetime = datetime.datetime.strptime(item['published_at'], "%Y-%m-%d %H:%M:%S")
            if published_at_2_datetime.year > nt.year:
                correct_date = published_at_2_datetime.replace(year=nt.year).strftime("%Y-%m-%d %H:%M:%S")
                item['published_at'] = correct_date

        # TODO(coder.gsy@gmail.com): 改换成 ItemLoader 作数据预处理。
        if not item['source']:
            item['source'] = u''

        # 入库
        # queryset = self.session.query(Articles).filter(Articles.article_id == item['article_id']).first()
        # if not queryset:
        #     self.session.add(Articles(created_time=nt, last_updated=nt, **item))
        # else:
        #     queryset.comments = item['comments']
        #     queryset.share = item['share']
        #     queryset.last_updated = nt
        #     if item.get('visit_total'):
        #         queryset.visit_total = item['visit_total']
        # self.session.commit()
        if len(self.results) >= 100:
            self.session.bulk_save_objects(self.results)
            self.results = []
        self.session.commit()
        return item

    def close_spider(self, spider):  # 上下文管理
        if self.results:
            self.session.bulk_save_objects(self.results)
        self.session.commit()

        self.session.close()
