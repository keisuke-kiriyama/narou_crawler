import scrapy

from narou_crawler.items import NCodeItem

class NCodeSpider(scrapy.Spider):
    name = 'narou_ncode_spider'
    allowed_domains = ['yomou.syosetu.com',
                       'mypage.syosetu.com',
                       'ncode.syosetu.com']
    start_urls = ['https://yomou.syosetu.com/userlist/avgranklist/?p=1']


    def parse(self, response):
        for url in response.xpath('//span[@class="username"]/a/@href').extract():
            yield scrapy.Request(url, callback=self.parse_mypage)
        next_page_url = response.xpath('//div[@class="navi_all"]/a[@title="次のページ"]/@href').extract_first()
        yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def parse_mypage(self, response):
        novel_list_url = response.xpath('//div[@class="a_line"]/a[contains(text(), "作品一覧")]/@href').extract_first()
        yield scrapy.Request(response.urljoin(novel_list_url), callback=self.parse_novel_list)

    def parse_novel_list(self, response):
        ncode_item = NCodeItem()
        for url in response.xpath('//p[@class="info"]/a[contains(text(), "小説情報")]/@href').extract():
            ncode_item['n_code'] = url.split('/')[-2]
            yield ncode_item
        next_page_url = response.xpath('//div[@class="pager_idou"]/a[@title="next page"]/@href').extract_first()
        yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_novel_list)
