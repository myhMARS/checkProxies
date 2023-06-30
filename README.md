# checkProxies
获取代理，通过python爬虫的方式爬取socks4\socks5\http\https的代理并进行检测是否可用


## 环境配置
```angular2html
pip install -r requirement.txt
```
## 使用说明
程序默认爬取IP源为中国区域，如需调整可运行 `Proxies.place()` 函数进行国家修改

检测IP可用性地址为 *baidu.com* 如有访问外网需求可修改 Proxies 类中的 *check_url* 值
```
python
>>> form getProxies import *
>>> obj = Proxies()
>>> obj.getIPs()
>>> obj.checks()
>>> obj.list_output() # 以列表格式返回(IP,Port)
>>> obj.file_output() # 以文件形式返回，支持提供IP地理位置(需将ip_flag设为True)
```
程序运行后将在目录下生成一个对应txt文件包含获得的IP

中国境内IP支持具体位置查询 




