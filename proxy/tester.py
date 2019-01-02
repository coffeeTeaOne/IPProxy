import asyncio
import aiohttp
import time
import sys

from ProxyLog.logger import ProxyLogger
from proxy.db_redis import RedisClient
from proxy.getter import Getter

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError


class Tester(object):
    # 普通池
    TEST_URL = 'https://www.baidu.com/'
    # 微信池
    # TEST_URL = 'http://weixin.sogou.com/weixin'

    def __init__(self, total):
        """
        实例化
        :param total:池总数
        """
        self.total = total
        self.proxy_getter = Getter()
        self.redis = RedisClient()
        self.log = ProxyLogger().logger
    
    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                # self.log.info('正在测试：' + proxy)
                async with session.get(self.TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=False) as response:
                    if response.status not in [200, 302]:
                        self.redis.del_ip(proxy)
                        # print('请求响应码不合法 ', response.status, 'IP', proxy)
                        proxies = self.redis.get_all()
                        if len(proxies) < self.total:
                            self.again_get_ip(proxies)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.del_ip(proxy)
                # self.log.info('代理请求失败:' + proxy)
                proxies = self.redis.get_all()
                if len(proxies) < self.total:
                    self.again_get_ip(proxies)

    def again_get_ip(self, proxies):
        """
        重新获取ip
        :param proxies:
        :return:
        """
        # log = ProxyLogger().logger
        count = 1
        while True:
            ip = self.proxy_getter.run()
            if ip:
                if ip in proxies:
                    count += 1
                    continue
                elif count > 5:
                    self.log.error('没有获取到可用ip！')
                    # log.handlers.clear()
                    return False
                else:
                    # self.log.info('重新获取的ip:' + ip)
                    self.redis.save(ip)
                    break
            else:
                time.sleep(5)
                continue

    def run(self):
        """
        测试主函数
        :return:
        """
        # log.info('测试器开始运行!')
        try:
            count = self.redis.get_count()
        except:
            print(4)
            self.log.error('数据库连接错误！')
            return False
        # print('当前剩余' + str(count) + '个代理')
        mid_num = self.total - count
        if mid_num > 0:
            while mid_num:
                all_proxies = self.redis.get_all()
                self.again_get_ip(all_proxies)
                mid_num -= 1
        try:
            test_proxies = self.redis.get_all()
            # self.log.info('池里的ip:' + ','.join(test_proxies))
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
            sys.stdout.flush()
            return True
        except Exception as e:
            self.log.error('测试器发生错误:' + str(e.args))
            return False


if __name__ == '__main__':
    Tester(total=3).run()
