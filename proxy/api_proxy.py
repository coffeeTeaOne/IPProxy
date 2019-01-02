import random

import requests
import time

from ProxyLog.logger import ProxyLogger


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):

    def __init__(self):
        self.log = ProxyLogger().logger

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            # print('成功获取到代理', proxy)
            # self.log.info('成功获取到代理:' + proxy)
            proxies.append(proxy)
        return proxies

    def crawl_proxy_29(self):
        """
        29代理获取
        :return:
        """
        # log = ProxyLogger().logger
        url_29 = 'http://183.131.114.29:9003/api/ip/get'
        try:
            res = requests.get(url=url_29).json()
        except:
            print(2)
            self.log.error('29代理请求外部接口网络异常!')
            return False
        if res.get('status') == 400:
            time.sleep(30)
            count = 0
            while True:
                if count < 11:
                    time.sleep(2)
                    try:
                        res = requests.get(url=url_29).json()
                    except:
                        count += 1
                        continue
                    if res.get('status') == 200:
                        break
                    else:
                        count += 1
                        continue
                else:
                    print(2)
                    self.log.error('29代理延时请求外部接口网络异常!')
                    return False
        ip = eval(res.get('result')).get('proxy')
        user_pass = eval(res.get('result')).get('user_pass')
        if ip:
            output_ip = '%s@%s' % (user_pass, ip)
            yield output_ip
        else:
            print(2)
            self.log.error('29代理外部接口没有获取到ip!')
            return False

    def crawl_proxy_fast(self):
        """
        快代理获取
        :return:
        """
        # log = ProxyLogger().logger
        url_fast = 'http://dps.kdlapi.com/api/getdps/?orderid=984423689516359&num=1&pt=1&ut=1&format=json&sep=1'
        try:
            time.sleep(random.randint(1, 2))
            res = requests.get(url=url_fast).json()
        except:
            print(2)
            self.log.error('快代理外部接口获取ip异常！')
            return False
        ips = list(res.get('data').get('proxy_list'))
        if ips:
            yield ips[0]
        else:
            print(2)
            self.log.error('快代理外部接口获取ip异常！')
            return False

    # def crawl_proxy_wandou(self):
    #     """
    #     豌豆代理获取
    #     :return:
    #     """
    #     # log = ProxyLogger().logger
    #     url_wandou = r'http://h.wandouip.com/get/ip-list?pack=840&num=1&xy=1&type=2&lb=\r\n&mr=2&'
    #     try:
    #         time.sleep(random.randint(1, 2))
    #         re = requests.get(url=url_wandou).json()
    #     except:
    #         print(2)
    #         self.log.error('豌豆代理外部接口获取ip异常！')
    #         return False
    #     i = re.get('data')[0]
    #     ip = '{ip}:{port}'.format(ip=i.get('ip'), port=i.get('port'))
    #     yield ip


if __name__ == '__main__':
    Crawler().get_proxies(0)
