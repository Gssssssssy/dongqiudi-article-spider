# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DongQiuDiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_id = scrapy.Field()
    label = scrapy.Field()
    title = scrapy.Field()
    writer = scrapy.Field()
    body = scrapy.Field()
    comments = scrapy.Field()
    share = scrapy.Field()
    tags = scrapy.Field()
    source = scrapy.Field()
    visit_total = scrapy.Field()
    published_at = scrapy.Field()
    href = scrapy.Field()
