import difflib
import os
import re
import sys
import time

import requests
from lxml import etree


def main():
    url = "https://freeproxyupdate.com"
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
    try:
        print("获取国家列表")
        req = requests.get(url, headers=headers)
    except:
        print("获取失败")
        sys.exit()
    req.encoding = 'utf-8'
    e = etree.HTML(req.text)
    urls = e.xpath("//body/div[4]/div/div/ul/li/a/@href")
    countries = e.xpath("//body/div[4]/div/div/ul/li/a//text()")
    print("获取成功")
    choose = input("选择国家方式:\n1.模糊搜索\n2.列表选取\nchoose:")
    # 模糊搜索
    if choose == '1':
        while True:
            os.system('cls')
            country = input("输入国名(英语):")
            res = difflib.get_close_matches(country, countries, 10, cutoff=0.55)
            if len(res) == 0:
                continue
            for i in range(len(res)):
                print(f"{i+1}.{res[i]}")
            try:
                choose = int(input("choose:"))
            except ValueError:
                print("非法输入")
                time.sleep(1)
                continue
            x = countries.index(str(res[choose-1]))
            flag = True
            if countries[x] != "China":
                flag = False
            write_auto(str(urls[x]), flag)
            break
    elif choose == '2':
        os.system('cls')
        for i in range(len(countries)):
            if i % 10 == 0:
                print(f"请输入选择国家的编号(n下一页,e退出){i//10+1}/{len(countries)//10+1}")
            print(f"{i+1}.{countries[i]}")
            if (i+1) % 10 == 0:
                x = input("number:")
                if x == "n":
                    os.system('cls')
                elif x == "e":
                    os.system('cls')
                    print('退出')
                    break
                elif x.isnumeric() and len(countries) >= int(x) > 0:
                    os.system('cls')
                    flag = True
                    if countries[i] != "China":
                        flag = False
                    write_auto(str(urls[i]), flag)
                    break
                else:
                    print('非法输入')
                    break


# 实现对main.py文件的自动修改
def write_auto(country, flag):
    f = open('main.py', 'r', encoding='utf-8')
    a = f.read()
    s1 = re.sub(r"country = .+", f"country = '{country}'", a, 1)
    s2 = re.sub(r"ip_flag = .+", f"ip_flag = {flag}", s1, 1)
    f = open('main.py', 'w', encoding='utf-8')
    f.write(s2)
    f.close()
    print("写入完成")


if __name__ == "__main__":
    main()
