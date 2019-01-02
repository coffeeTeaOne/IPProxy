
import sys
import io
import time

from ProxyLog.logger import ProxyLogger
from proxy.tester import Tester

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

log = ProxyLogger().logger


def main():
    max_num = 8
    log.info('开始运行---')
    # max_num = int(sys.argv[1])
    try:
        while True:
           flag = Tester(max_num).run()
           if flag:
               print(0)
               log.info('success')
           else:
               print(9)
               log.error('failed')
           time.sleep(5)
    except Exception as e:
        print(5)
        log.error(e.args)
        # main()


if __name__ == '__main__':
    main()
