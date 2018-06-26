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
        start_urls = []
        with open(settings.get('START_URLS_FILE_PATH')) as f:
            for line in f.readlines():
                n_code = line.split(',')[1].replace('"', '').strip()
                start_urls.append('https://ncode.syosetu.com/' + n_code + '/')
        self.start_urls = start_urls

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)

    def parse(self, response):
        n_code = response.url.split('/')[-2]
        contents = response.xpath('//div[@id="novel_honbun"]/p/text()').extract()
        novel_contents = NovelContents()
        novel_contents['n_code'] = n_code
        novel_contents['contents'] = []
        if contents:
            novel_contents['sub_titles'] = response.xpath('//p[@class="novel_title"]/text()').extract()
            novel_contents['contents'].append(contents)
            yield novel_contents
        else:
            novel_contents['sub_titles'] = response.xpath('//dd[@class="subtitle"]/a/text()').extract()
            first_sublist_url = response.urljoin(response.xpath('//dl[@class="novel_sublist2"]/dd/a/@href').extract_first())
            request = scrapy.Request(first_sublist_url, callback=self.parse_content)
            request.meta['novel_contents'] = novel_contents
            yield request

    def parse_content(self, response):
        novel_contents = response.meta['novel_contents']
        novel_content = response.xpath('//div[@id="novel_honbun"]/p/text()').extract()
        novel_contents['contents'].append(novel_content)
        next_page_url = response.xpath(u'//div[@class="novel_bn"]/a[contains(text(), "次へ")]/@href').extract_first()
        if next_page_url:
            request = scrapy.Request(response.urljoin(next_page_url), callback=self.parse_content)
            request.meta['novel_contents'] = novel_contents
            yield request
        else:
            yield novel_contents


