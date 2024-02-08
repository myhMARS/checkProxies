import json
import threading
import time
import requests
import jsonpath
import logging
from rich.progress import track


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s',
                    level=logging.INFO)


def _format_ips(ip, protocol):
    proxies = dict()
    if protocol != 'http' and protocol != "https":
        proxies['http'] = f'{protocol}://{ip}'
        proxies['https'] = f'{protocol}://{ip}'
    else:
        proxies['http'] = f'{ip}'
        proxies['https'] = f'{ip}'
    return proxies


class Proxies:
    def __init__(self):
        self.url = "https://openproxylist.xyz/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                          ' like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        self.ips = []
        self.times = []
        self.threads = []
        self.useful = 0
        self.flag = []
        self.api_time_limit = 0
        with open('IPs.txt', 'w', encoding='utf-8') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            f.write('\n')
        self.getIPs()

    def getIPs(self):
        protocols = ['socks4', 'socks5', 'http']
        for protocol in protocols:
            try:
                page = requests.get(self.url + protocol + '.txt', headers=self.headers)
            except:
                logging.error(f'获取代理池{protocols}失败')
            else:
                page.encoding = 'utf-8'
                self.ips = page.text.split('\n')
                self.flag = [False] * len(self.ips)
                self.times = [0] * len(self.ips)
                logging.info(f'获取到{protocol}，类型ip{len(self.ips)}个')
                self.checks(protocol)
                self.file_output(protocol)

    def checks(self, protocol, check_url="https://httpbin.org/get"):
        index = 0
        logging.info(f'正在启动检测线程')
        for ip in track(self.ips):
            if ip == '':
                continue
            thread_obj = threading.Thread(target=self._check, args=(index, ip, protocol, check_url))
            self.threads.append(thread_obj)
            thread_obj.start()
            index += 1
        logging.info(f'检测开始')
        for _ in track(self.threads):
            _.join()
        logging.info(f'协议{protocol}获取到可用地址数:{self.flag.count(True)}')

    def _check(self, index, ip, protocol, check_url):
        proxies = _format_ips(ip, protocol)
        requests.packages.urllib3.disable_warnings()
        try:
            cost_time = requests.get(check_url, proxies=proxies, verify=False, headers=self.headers, timeout=3).text
            self.flag[index] = True
            self.times[index] = cost_time
        except:
            pass

    def file_output(self, protocol):
        with open('IPs.txt', 'a', encoding='utf-8') as f:
            logging.info('正在输出至文本')
            for i in track(range(len(self.flag))):
                if self.flag[i]:
                    self.useful += 1
                    f.write("IP地址:" + '%-27s' % self.ips[i] +
                            "协议:" + '%-15s' % protocol +
                            "延迟:" + '%-12s' % str(self.times[i]) +
                            "地址:" + '%-50s' % str(self.__ip_info(str(self.ips[i]))) +
                            "\n")

    def list_output(self):
        res = []
        for i in range(len(self.ips)):
            if self.flag[i]:
                res.append((self.ips[i]))
        return res

    def __ip_info(self, ip):
        try:
            ip, _ = ip.split(':')
        except ValueError:
            print(f'error: {ip}')
            return None
        if self.api_time_limit == 10:
            time.sleep(0.5)
        url = " https://tools.mgtv100.com/external/v1/ips/query?ip="
        # 感谢夏柔api提供的api服务  https://api.aa1.cn/
        req = requests.get(url + ip)
        req.encoding = "utf-8"
        try:
            data = json.loads(req.text)
        except:
            time.sleep(0.5)
            return self.__ip_info(ip)
        country = jsonpath.jsonpath(data, "$..country")
        province = jsonpath.jsonpath(data, "$..state_name")
        city = jsonpath.jsonpath(data, "$..city")
        self.api_time_limit += 1
        return [country[0], city[0], province[0]]


if __name__ == '__main__':
    obj = Proxies()
