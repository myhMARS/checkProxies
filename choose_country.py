import requests
from lxml import etree
import os
import sys
import difflib


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
    choose = input("选择国家方式:\n1.模糊搜索（未完成）\n2.列表选取\nchoose:")
    if choose == '1':
        # TODO: 模糊搜索demo(未完成)
        os.system('cls')
        country = input("输入国名(英语):")
        res = difflib.get_close_matches(country, countries, 4, cutoff=0.6)
        print(res)
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
                    print("请手动修改main.py中setting函数中country值为'"+urls[i]+"'")
                    if countries[i] != "China":
                        print("ip_flag = False")
                    break
                else:
                    print('非法输入')
                    break


if __name__ == "__main__":
    main()
