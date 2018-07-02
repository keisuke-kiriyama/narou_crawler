# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import os
import json
import gzip
from urllib.request import urlopen

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

    PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
    DATA_DIR_PATH = os.path.join(PROJECT_ROOT, 'data')
    CONTENTS_DIR_PATH = os.path.join(DATA_DIR_PATH, 'contents')
    META_DIR_PATH = os.path.join(DATA_DIR_PATH, 'meta')

    def process_item(self, item, spider):
        if not spider.name == 'narou_contents_spider':
            return item

        if not item['n_code']:
            raise DropItem('Missing n_code')

        output_file_path = os.path.join(self.CONTENTS_DIR_PATH, item['n_code'] + '.json')
        with open(output_file_path, 'w') as f:
            json.dump(dict(item), f, ensure_ascii=False)

        self.fetch_novel_meta_info(item['n_code'])
        return item

    def fetch_novel_meta_info(self, n_code):
        url = 'https://api.syosetu.com/novelapi/api/?out=json&gzip=5&of=t-n-u-w-s-bg-g-k-nt-e-ga-l-gp-f-r-a-ah-ka-&lim=1&ncode={}'.format(n_code)
        print("fetch novel_meta: {}".format(url))
        response = urlopen(url)
        output_file_path = os.path.join(self.META_DIR_PATH, n_code + '_meta.json')
        try:
            with gzip.open(response, 'rt', encoding='utf-8') as f:
                j_raw = f.read()
                j_obj = json.loads(j_raw)
                novel_meta = j_obj[1]
                with open(output_file_path, 'w') as f:
                    json.dump(novel_meta, f, ensure_ascii=False)

        except:
            print("error to write meta: {}".format(n_code))

