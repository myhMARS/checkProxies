import requests
import sys
import time
from lxml import etree
import logging
import threading
import json
import jsonpath
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
logging.disable()


global country, ip_flag, check_url, headers


def setting():
    global country, ip_flag, check_url, headers
    # 如需访问google可更改check_url为谷歌网址
    # check_url = "https://wwww.google.com"
    check_url = "https://www.baidu.com"
    # ip_flag用于开启ip位置查询服务，目前仅支持中国地区查询非中国区域请设置为False
    ip_flag = True
    country = "/china-cn"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }


def main():
    url = f"https://freeproxyupdate.com{country}"
    # 连接代理池
    print('连接代理池......')
    try:
        req = requests.get(url, headers=headers)
        print('连接成功')
    except Exception:
        print('连接失败')
        sys.exit()
    # 初始化文本文件
    with open("IP代理.txt", 'w') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        f.write('\n')
    req.encoding = 'utf-8'
    e = etree.HTML(req.text)
    number = e.xpath("//strong/text()")
    print(f"抓取到代理IP{number[0]}个")
    number = int(number[0])
    useful = 0
    for x in range(1, number // 100 + 2):
        print(f"检测第{x}页IP，共计{number // 100 + 1}页")
        page_url = f"https://freeproxyupdate.com/china-cn/page-{str(x)}"
        try:
            page = requests.get(page_url, headers=headers)
        except:
            print(f"连接第{x}页失败")
            continue
        page.encoding = 'utf-8'
        e = etree.HTML(page.text)
        ip = e.xpath("//table[3]/tbody/tr/td[1]/text()")
        port = e.xpath("//table[3]/tbody/tr/td[2]/text()")
        # 使用xpath的//text方法提取协议及匿名度
        protocol = e.xpath("//tbody/tr/td[5]//text()")
        anonymity = e.xpath("//tbody/tr/td[6]//text()")
        # 多线程处理
        ip_num = len(ip)
        flag = [0]*ip_num
        j = 0
        threads = []
        for i, p, pr, an in zip(ip, port, protocol, anonymity):
            thread_obj = threading.Thread(target=check, args=(j, flag, i, p, pr))
            threads.append(thread_obj)
            thread_obj.start()
            j += 1
        # 等待线程结束
        for thread in threads:
            thread.join()
        with open("IP代理.txt", 'a') as f:
            for i in range(ip_num):
                if flag[i] == 1:
                    useful += 1
                    f.write("IP地址:" + '%-18s' % ip[i] + "端口:" + '%-6s' % port[i] + "协议:" + '%-9s' % protocol[i] +
                            "匿名:" + '%-10s' % anonymity[i] + "地址:" + '%-30s' % str(ipinfo(ip[i])) + "\n")
            f.close()
    print('\n')
    print(f"{number}个IP检测完毕,抓取到可用IP{useful}个")


def check(i, flag, ip, port, protocol):
    proxies = dict()
    if protocol != 'http' and protocol != "https":
        proxies['http'] = f'{protocol}://{ip}:{port}'
        proxies['https'] = f'{protocol}://{ip}:{port}'
    else:
        proxies['http'] = f'{ip}:{port}'
        proxies['https'] = f'{ip}:{port}'
    requests.packages.urllib3.disable_warnings()
    try:
        requests.get(check_url, proxies=proxies, verify=False, headers=headers, timeout=5)
        flag[i] = 1
    except Exception:
        pass


def ipinfo(ip):
    if not ip_flag:
        return country[1:]
    url = "https://zj.v.api.aa1.cn/api/chinaip/?ip="
    # 感谢夏柔api提供的api服务  https://api.aa1.cn/
    req = requests.get(url + ip)
    req.encoding = "utf-8"
    data = json.loads(req.text)
    # print(json.dumps(data, sort_keys=True, indent=2))
    province = jsonpath.jsonpath(data, "$..Province")
    city = jsonpath.jsonpath(data, "$..City")
    isp = jsonpath.jsonpath(data, "$..isp")
    district = jsonpath.jsonpath(data, "$..District")
    return [province[0], city[0], district[0], isp[0]]


if __name__ == "__main__":
    setting()
    main()
