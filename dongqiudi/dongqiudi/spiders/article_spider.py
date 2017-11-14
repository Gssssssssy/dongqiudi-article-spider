# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import lxml.html
from scrapy import Spider
from scrapy.http import Request

from ..items import DongQiuDiItem


class DongQiuDiSpider(Spider):
    name = 'article'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5X Build/N2G48C; wv) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Version/4.0 Chrome/60.0.3112.116 Mobile Safari/537.36 News/127 Android/127 '
                      'NewsApp/127 SDK/25 '
    }
    count = 0
    baseline = 100    # 基线条件

    # TODO(coder.gsy@gmail.com): 完成五大联赛等 Tabs 的爬取。
    def start_requests(self):
        headline_url = 'https://api.dongqiudi.com/app/tabs/android/1.json'
        yield Request(headline_url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        self.count += 1
        data = json.loads(response.body)
        if data.get('articles'):
            articles = data.get('articles')    # 获取文章列表
            for i, article in enumerate(articles):
                item = DongQiuDiItem()
                item['label'] = data.get('label', '')
                item['article_id'] = article.get('id')
                item['title'] = article.get('title')
                item['comments'] = article.get('comments_total')
                item['published_at'] = article.get('published_at')

                if article.get('id'):
                    detail_url = 'https://api.dongqiudi.com/v2/article/detail/{art_id}'.format(art_id=article.get('id'))
                    yield Request(detail_url, callback=self.parse_article_detail, meta={'item': item},
                                  headers=self.headers)

        if data.get('next'):
            while self.count < self.baseline:    # 递归条件
                headline_url = data.get('next')
                yield Request(headline_url, callback=self.parse, headers=self.headers)   # 递归抓取

    def parse_article_detail(self, response):
        data = json.loads(response.body)
        data = data.get('data')
        if data.get('infos'):
            info = data.get('infos')
            item = response.meta['item']
            channels = info.get('channels', [])
            item['tags'] = self.extract_relative_tags(channels)
            item['writer'] = data.get('writer', '')
            item['source'] = data.get('source', '')
            item['body'] = self.clean_article_html_tags(data.get('body', ''))
            if data.get('visit_total'):
                item['visit_total'] = data.get('visit_total')
            share_url = 'https://api.dongqiudi.com/share/list/article/{art_id}'.format(art_id=item['article_id'])
            yield Request(share_url, callback=self.parse_article_share_link, meta={'item': item})

    @staticmethod
    def parse_article_share_link(response):
        data = json.loads(response.body)
        share_count = data.get('total', 0)
        item = response.meta['item']
        item['share'] = share_count
        yield item

    @staticmethod
    def extract_relative_tags(channels):
        """
        从 `channels` 数组内提取每个 tag 并拼接成单个字符串
        :param channels: 相关 tags 数组
        :return: tags 字符串
        """
        tag_list = [channel.get('tag', '') for channel in channels]
        return ';'.join(tag_list)

    # TODO(coder.gsy@gmail.com): 改换成 ItemLoader 作数据预处理。
    @staticmethod
    def clean_article_html_tags(text):
        """
        移除文章内容里的 HTML 标签
        :param text: HTML 文本
        :return:
        """
        return lxml.html.fromstring(text).text_content()
