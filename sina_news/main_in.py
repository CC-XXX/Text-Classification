from scrapy import cmdline
import os
import time

if __name__ == '__main__':
     # os.system('pwd')
    while True:
        os.system("scrapy crawl news_spi")
        # 每２个小时执行一次　６０＊６０＊２
        time.sleep(1200)

#cmdline.execute('scrapy crawl news_spi'.split())