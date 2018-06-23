import scrapy
from scrapy_splash import SplashRequest
import json
from urllib.request import urlopen, HTTPError, URLError
import gzip

from narou_crawler.items import NovelInfo

class NarouMetaSpider(scrapy.Spider):
    name = 'narou_meta_spider'
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
        yield SplashRequest(response.urljoin(next_page_url), self.parse_novel_list, args={'wait': 1.0})

    def parse_novel_info(self, response):
        novel = NovelInfo()
        n_code = response.xpath('//p[@id="ncode"]/text()').extract_first()
        novel_meta = self.fetch_novel_meta_info(n_code)
        if not novel_meta or not novel_meta['ncode'] == n_code: return
        novel['n_code'] = n_code
        novel['title'] = novel_meta['title']
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
        novel['all_eval_count'] = novel_meta['all_hyoka_cnt']
        novel['talk_rate'] = novel_meta['kaiwaritu']
        novel['user_id'] = novel_meta['userid']
        novel['writer'] = novel_meta['writer']
        yield novel

    def fetch_novel_meta_info(self, n_code):
        url = 'http://api.syosetu.com/novelapi/api/?out=json&gzip=5&of=t-n-u-w-s-bg-g-k-nt-e-ga-l-gp-f-r-a-ah-ka-&lim=1&ncode={}'.format(n_code)
        error_log_file_path = './data/fetch_error_log.txt'
        f = open(error_log_file_path, 'a')
        novel_meta = None
        try:
            response = urlopen(url)
            with gzip.open(response, 'rt', encoding='utf-8') as f:
                j_raw = f.read()
                j_obj = json.loads(j_raw)
                novel_meta = j_obj[1]
        except HTTPError as err:
            f.write("Ncode: {}, HTTPError: {}".format(n_code, err))
            f.close()
        except URLError as err:
            f.write("Ncode: {}, URLError: {}".format(n_code, err))
            f.close()
        except:
            f.write("Ncode: {}, Erorr".format(n_code))
            f.close()
        return novel_meta

if __name__ == '__main__':
    spider = NarouMetaSpider()
    novel_meta = spider.fetch_novel_meta_info('N2415EG')

