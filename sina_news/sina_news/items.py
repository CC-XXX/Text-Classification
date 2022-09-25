# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    time_stamp = scrapy.Field() #时间
    news = scrapy.Field()       #新闻
    tag1 = scrapy.Field()       #新浪分类标记
    tag2 = scrapy.Field()
    tag3 = scrapy.Field()
    tag4 = scrapy.Field()
    tag5 = scrapy.Field()
    update_time_flag = scrapy.Field()  #更新的时间标记
