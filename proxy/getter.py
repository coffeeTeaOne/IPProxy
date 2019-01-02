import random

from ProxyLog.logger import ProxyLogger
from proxy.db_redis import RedisClient
from proxy.api_proxy import Crawler

import sys


class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.redis.get_count() >= 5:
            return True
        else:
            return False
    
    def run(self):
        # self.log.info('获取器开始执行！')
        # all_proxies = []
        # 循环获取代理接口
        # for callback_label in range(self.crawler.__CrawlFuncCount__):
        # 随机获取代理接口
        callback_label = random.randint(0, self.crawler.__CrawlFuncCount__-1)
        callback = self.crawler.__CrawlFunc__[callback_label]
        # callback = self.crawler.__CrawlFunc__[0]
        # 获取代理
        proxies = self.crawler.get_proxies(callback)
        sys.stdout.flush()
        # ip = random.choice(all_proxies)
        if proxies:
            return proxies[0]
        else:
            return None


if __name__ == '__main__':
    print(Getter().run())
