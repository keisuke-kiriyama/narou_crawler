# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json
from urllib.request import urlopen
import gzip

from narou_crawler.items import Novel

class NarouSpider(scrapy.Spider):
    name = 'narou_spider'
    allowed_domains = ['yomou.syosetu.com',
                       'mypage.syosetu.com',
                       'ncode.syosetu.com']
    start_urls = ['https://yomou.syosetu.com/userlist/avgranklist/?p=1']

    def parse(self, response):
        for url in response.xpath('//span[@class="username"]/a/@href').extract():
            yield SplashRequest(url, self.parse_mypage, args={'wait': 1.0})
        next_page_url = response.xpath('//div[@class="navi_all"]/a[@title="次のページ"]/@href').extract_first()
        yield SplashRequest(response.urljoin(next_page_url), self.parse, args={'wait': 1.0})


    def parse_mypage(self, response):
        novel_list_url = response.xpath('//div[@class="a_line"]/a[contains(text(), "作品一覧")]/@href').extract_first()
        yield SplashRequest(response.urljoin(novel_list_url), self.parse_novel_list, args={'wait': 1.0})

    def parse_novel_list(self, response):
        for novel_info in response.xpath('//p[@class="info"]/a[contains(text(), "小説情報")]/@href').extract():
            yield SplashRequest(response.urljoin(novel_info), self.parse_novel_info, args={'wait': 1.0})
        next_page_url = response.xpath('//div[@class="pager_idou"]/a[@title="next page"]/@href').extract_first()
        yield SplashRequest(response.urljoin(next_page_url), self.parse_novel_list(), args={'wait': 1.0})

    def parse_novel_info(self, response):
        novel = Novel()
        n_code = response.xpath('//p[@id="ncode"]/text()').extract_first()
        novel_meta = self.fetch_novel_meta_info(n_code)
        if not novel_meta['ncode'] == n_code: return
        novel['title'] = novel_meta['title']
        novel['n_code'] = n_code
        novel['story'] = novel_meta['story']
        novel['big_genre'] = novel_meta['biggenre']
        novel['genre'] = novel_meta['genre']
        novel['keyword'] = novel_meta['keyword']
        novel['novel_type'] = novel_meta['noveltype']
        novel['end'] = novel_meta['end']
        novel['general_all_no'] = novel_meta['general_all_no']
        novel['length'] = novel_meta['length']
        novel['global_point'] = novel_meta['global_point']
        novel['fav_novel_count'] = novel_meta['fav_novel_cnt']
        novel['review_count'] = novel_meta['review_cnt']
        novel['all_point'] = novel_meta['all_point']
        novel['all_hyoka_count'] = novel_meta['all_hyoka_cnt']
        novel['talk_rate'] = novel_meta['kaiwaritu']
        novel['user_id'] = novel_meta['userid']
        novel['writer'] = novel_meta['writer']
        # novel['n_code'] = response.xpath('//p[@id="ncode"]/text()').extract_first()
        # novel['title'] = response.xpath('//div[@id="contents_main"]/h1/a/text()').extract_first()
        # novel['story'] = response.xpath('//td[@class="ex"]/text()').extract()
        # novel['genre'] = response.xpath('//th[contains(text(), "ジャンル")]/following-sibling::td/text()').extract()
        # novel['keyword'] = response.xpath('//th[contains(text(), "キーワード")]/following-sibling::td/span/text()').extract() + \
        #                    response.xpath('//th[contains(text(), "キーワード")]/following-sibling::td/text()').extract()

    def fetch_novel_meta_info(self, n_code):
        url = 'http://api.syosetu.com/novelapi/api/?out=json&gzip=5&of=t-n-u-w-s-bg-g-k-nt-e-ga-l-gp-f-r-a-ah-ka-&lim=1&ncode={}'.format(n_code)
        response = urlopen(url)
        with gzip.open(response, 'rt', encoding='utf-8') as f:
            j_raw = f.read()
            j_obj = json.loads(j_raw)
        return j_obj[1]

if __name__ == '__main__':
    spider = NarouSpider()
    novel_meta = spider.fetch_novel_meta_info('N2415EG')
    print(novel_meta)

