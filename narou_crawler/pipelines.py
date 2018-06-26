# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class NCodeItemValidationPipeline(object):
    def process_item(self, item, spider):
        if not spider.name == 'narou_ncode_spider':
            return item

        if not item['n_code']:
            raise DropItem('Missing n_code')

        if not item['n_code'][0] == 'n':
            raise DropItem('not start n')

        return item


class NovelInfoValidationPipeline(object):
    def process_item(self, item, spider):
        if not spider.name == 'narou_meta_spider':
            return item

        if not item['n_code']:
            raise DropItem('Missing n_code')

        if not item['title']:
            raise DropItem('Missing title' + item['n_code'])

        if not item['story']:
            raise DropItem('Missing story' + item['n_code'])

        if not item['novel_type']:
            raise DropItem('Missing novel type' + item['n_code'])

        if not item['length']:
            raise DropItem('Missing length' + item['n_code'])

        return item

class NovelContentsValidationPipeline(object):
    def process_item(self, item, spider):
        if not spider.name == 'narou_contents_spider':
            return item

        if not item['n_code']:
            raise DropItem('Missing n_code')

        return item

