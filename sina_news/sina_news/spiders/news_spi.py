# -*- coding: utf-8 -*-
import scrapy
import json
from sina_news.items import SinaNewsItem
import re
import logging


class NewsSpiSpider(scrapy.Spider):
    name = 'news_spi'
    #allowed_domains = ['sina.com']
    #start_urls = ['http://sina.com/']

    my_headers={
        'Referer': 'https://finance.sina.com.cn/',
        'Sec-Fetch-Mode': 'no-cors',
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'
    }


    page = 1
    timeflag = 0

    def start_requests(self):
        # 综合新闻
        need_page = 2
        for i in range(1,need_page):
            self.page = i
            url = 'https://zhibo.sina.com.cn/api/zhibo/feed?zhibo_id=152&id=&tag_id=0&page_size=30&type=0&page='+str(i)
            # 这是分类的新闻
            url2 = 'http://zhibo.sina.com.cn/api/zhibo/feed?page=1&page_size=20&zhibo_id=152&tag_id=0&dire=f&dpc=1&pagesize=20&type=0'
            yield scrapy.Request(url, headers=self.my_headers, callback=self.parse_info,meta={'page':i,'total_page':need_page})
            #yield scrapy.Request(url2, headers=self.my_headers, callback=self.parse_info)


    def parse_info(self, response):
        items = SinaNewsItem()
        origin_text=response.text.replace('try{t15701739(','').replace(');}catch(e){};','')
        af_text = json.loads(origin_text)['result']['data']['feed']['list']
        cc = 0

        for i in af_text:
            if cc>10:
                break
            if self.timeflag==0 and self.page==1:
                items['update_time_flag'] = i['create_time']
                self.timeflag=1
            else:
                items['update_time_flag'] = None
            items['time_stamp'] = i['create_time']
            new_temp = i['rich_text'].replace('【', '').replace('】', '')
            items['news']=re.sub('（.*?）','',new_temp).strip()
            tagss = i['tag']
            count = 0
            for j in tagss:
                count += 1
                name = 'tag'+str(count)
                items[name]=j['name']
            #print(items)
            logging.info(items['time_stamp']+items['news'])
            cc+=1
            yield items