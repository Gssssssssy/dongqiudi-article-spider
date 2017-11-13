# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
from scrapy.exceptions import DropItem
import datetime

from .models import DBSession, Articles

reload(sys)
sys.setdefaultencoding('utf-8')

class DongQiuDiPipeline(object):
    def __init__(self):
        self.session = DBSession()
        self.article_id_seen = set()

    def process_item(self, item, spider):
        if item['article_id'] in self.article_id_seen:
            raise DropItem("Duplicate item found: %s" % item)
        self.article_id_seen.add(item['article_id'])

        nt = datetime.datetime.now()
        if item['published_at']:
            published_at_2_datetime = datetime.datetime.strptime(item['published_at'], "%Y-%m-%d %H:%M:%S")
            if published_at_2_datetime.year > nt.year:
                correct_date = published_at_2_datetime.replace(year=nt.year).strftime("%Y-%m-%d %H:%M:%S")
                item['published_at'] = correct_date

        if not item['source']:
            item['source'] = u''

        queryset = self.session.query(Articles).filter(Articles.article_id == item['article_id']).first()
        if not queryset:
            self.session.add(Articles(created_time=nt, last_updated=nt, **item))
        else:
            queryset.visit_total = item['visit_total']
            queryset.comments = item['comments']
            queryset.share = item['share']
            queryset.last_updated = nt
        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
