# checkProxies
获取代理，通过python爬虫的方式爬取socks4\socks5\http\https的代理并进行检测是否可用
## 环境配置
```angular2html
pip install -r requirement.txt
```
## 使用说明
程序默认爬取IP源为中国区域，如需调整可运行 *choose_country.py* 文件进行国家筛选

检测IP可用性地址为 *baidu.com* 如有访问外网需求可修改 *setting* 函数中的 *check_url* 值
```
python main.py
```
程序运行后将在目录下生成一个对应txt文件包含获得的IP

中国境内IP支持具体位置查询 

```angular2html
python choose_country.py
```
### To-do List
- [x] choose_country.py
  - [x] 支持从列表中筛选国家
  - [x] 支持模糊搜索国家
  - [x] 支持直接对 *main.py* 自动完成修改 



