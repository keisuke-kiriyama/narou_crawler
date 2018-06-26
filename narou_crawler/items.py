# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NCodeItem(scrapy.Item):
    n_code = scrapy.Field()

class NovelInfo(scrapy.Item):
    n_code = scrapy.Field()
    title = scrapy.Field()
    story = scrapy.Field()
    big_genre = scrapy.Field()
    genre = scrapy.Field()
    keyword = scrapy.Field()
    novel_type = scrapy.Field()
    end = scrapy.Field()
    general_all_no = scrapy.Field()
    length = scrapy.Field()
    global_point = scrapy.Field()
    fav_novel_count = scrapy.Field()
    review_count = scrapy.Field()
    all_point = scrapy.Field()
    all_eval_count = scrapy.Field()
    talk_rate = scrapy.Field()
    user_id = scrapy.Field()
    writer = scrapy.Field()

class NovelContents(scrapy.Item):
    n_code = scrapy.Field()
    contents = scrapy.Field()
