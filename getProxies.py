import json
import sys
import threading
import time
import difflib
import requests
import jsonpath
import os
from lxml import etree


def _format_ips(ip, port, protocol):
    proxies = dict()
    if protocol != 'http' and protocol != "https":
        proxies['http'] = f'{protocol}://{ip}:{port}'
        proxies['https'] = f'{protocol}://{ip}:{port}'
    else:
        proxies['http'] = f'{ip}:{port}'
        proxies['https'] = f'{ip}:{port}'
    return proxies


class Proxies:
    def __init__(self,ip_flag=False):
        self.url = "https://freeproxyupdate.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                          ' like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        self.ip_flag = ip_flag
        self.country = '/china-cn'
        self.ip = []
        self.port = []
        self.protocol = []
        self.anonymity = []
        self.threads = []
        self.useful = 0
        self.flag = None
        self._getPage()

    def _getPage(self):
        url = f'{self.url}{self.country}'
        try:
            req = requests.get(url, headers=self.headers)
            print('代理池连接成功')
        except:
            print('代理池连接失败')
            sys.exit()
        req.encoding = 'utf-8'
        self.page = req
        e = etree.HTML(req.text)
        num = int(e.xpath("//strong/text()")[0])
        self.page_num = num // 100 + 1

    def getIPs(self):
        for x in range(1, self.page_num + 1):
            page_url = f"{self.url}{self.country}/page-{str(x)}"
            try:
                page = requests.get(page_url, headers=self.headers)
            except:
                print(f'连接第{x}页失败')
                continue
            page.encoding = 'utf-8'
            e = etree.HTML(page.text)
            self.ip.extend(e.xpath("//table/tbody/tr/td[1]/text()"))
            self.port.extend(e.xpath("//table/tbody/tr/td[2]/text()"))
            self.protocol.extend(e.xpath("///table/tbody/tr/td[4]//text()"))
            self.anonymity.extend(e.xpath("//tbody/tr/td[5]//text()"))
        ip_num = len(self.ip)
        self.flag = [False] * len(self.ip)
        print(f'抓取到代理{ip_num}个')

    def checks(self,check_url="https://www.baidu.com"):
        index = 0
        for i, p, pr, an in zip(self.ip, self.port, self.protocol, self.anonymity):
            thread_obj = threading.Thread(target=self._check, args=(index, i, p, pr, check_url))
            self.threads.append(thread_obj)
            thread_obj.start()
            index += 1
        for _ in self.threads:
            _.join()

    def _check(self, index, ip, port, protocol, check_url):
        proxies = _format_ips(ip, port, protocol)
        requests.packages.urllib3.disable_warnings()
        try:
            requests.get(check_url, proxies=proxies, verify=False, headers=self.headers, timeout=3)
            self.flag[index] = True
        except:
            pass

    def file_output(self):
        with open('IPs.txt', 'w', encoding='utf-8') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            f.write('\n')
            for i in range(len(self.flag)):
                if self.flag[i]:
                    self.useful += 1
                    f.write("IP地址:" + '%-18s' % self.ip[i] + "端口:" + '%-6s' % self.port[i] + "协议:" + '%-9s' %
                            self.protocol[i] + "匿名:" + '%-10s' % self.anonymity[i] + "地址:" + '%-30s' %
                            str(self.ip_info(str(self.ip[i]))) + "\n")

    def list_output(self):
        res = []
        for i in range(len(self.ip)):
            if self.flag[i]:
                res.append((self.ip[i], self.port[i]))
        return res

    def place(self,model=1):
        e = etree.HTML(self.page.text)
        urls = e.xpath('//*[@id="side-column"]/div/ul/li/a/@href')
        countries = e.xpath('//*[@id="side-column"]/div/ul/li/a/text()')
        if model == 2:
            while True:
                country = input("输入国名(英语):")
                res = difflib.get_close_matches(country, countries, 10, cutoff=0.55)
                if len(res) == 0:
                    continue
                for i in range(len(res)):
                    print(f"{i + 1}.{res[i]}")
                try:
                    choose = int(input("choose:"))
                except ValueError:
                    print("非法输入")
                    time.sleep(1)
                    continue
                x = countries.index(str(res[choose - 1]))
                self.country = str(urls[x])
                if countries[x] != "China":
                    self.ip_flag = False
                break
        elif model == 1:
            for i in range(0,(len(countries)//10)*10+11,10):
                print(f"请输入选择国家的编号(n下一页,e退出){i // 10 + 1}/{len(countries) // 10 + 1}")
                for j in range(10):
                    try:
                        print(f"{j + 1}.{countries[i+j]}")
                    except:
                        break
                x = input("number:")
                if x == "n":
                    os.system('cls')
                elif x == "e":
                    os.system('cls')
                    print('退出')
                    return
                elif x.isnumeric() and 10 >= int(x) > 0:
                    os.system('cls')
                    self.country = str(urls[i+int(x)-1])
                    if countries[i] != "China":
                        self.ip_flag = False
                    break
                else:
                    print('非法输入')
                    return
        print('修改完成')

    def ip_info(self, ip):
        if not self.ip_flag:
            return self.country[1:]
        url = "https://zj.v.api.aa1.cn/api/chinaip/?ip="
        # 感谢夏柔api提供的api服务  https://api.aa1.cn/
        req = requests.get(url + ip)
        req.encoding = "utf-8"
        try:
            data = json.loads(req.text)
        except:
            time.sleep(0.5)
            return self.ip_info(ip)
        # print(json.dumps(data, sort_keys=True, indent=2))
        province = jsonpath.jsonpath(data, "$..Province")
        city = jsonpath.jsonpath(data, "$..City")
        isp = jsonpath.jsonpath(data, "$..isp")
        district = jsonpath.jsonpath(data, "$..District")
        return [province[0], city[0], district[0], isp[0]]
