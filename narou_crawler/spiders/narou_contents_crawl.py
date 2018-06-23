# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from narou_crawler.items import NovelContents

class NarouContentsSpider(scrapy.Spider):
    name = 'narou_contents_spider'
    allowed_domains = ['yomou.syosetu.com',
                       'mypage.syosetu.com',
                       'ncode.syosetu.com']
    start_urls = []

    def __init__(self, settings, *args, **kwargs):
        super(NarouContentsSpider, self).__init__(*args, **kwargs)
        print(settings.get('START_URLS_FILE_PATH'))
        # with open(settings.get('START_URLS_FILE_PATH')) as f:
        #     urls = f.readlines()
        # self.start_urls = urls

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)