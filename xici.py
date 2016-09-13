# -*- coding: UTF-8 -*-
import requests
# from openpyxl import Workbook
from lxml import etree

def get_proxies(ip,port):
    dict = {'http': 'http://%s:%d'%(ip,port)}
    return dict

def daili(xici):
    r = requests.get("http://www.rkpass.cn/u.jsp?u=309397", proxies=xici)
    print(r.status_code)

def get_result(page):
    html = requests.get('http://www.xicidaili.com/nt/'+str(page),headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
})
    ip_list = []
    port_list = []
    selector = etree.HTML(html.text)
    ip = selector.xpath('.//*[@class="odd"]/td[2]/text()')
    port = selector.xpath('.//*[@class="odd"]/td[3]/text()')
    for each in ip:
        ip_list.append(each)
    for each in port:
        port_list.append(each)

    nvs = zip(ip_list, port_list)
    nvDict = dict((name, value) for name, value in nvs)

    list_info = list(map(lambda x, y: (x, y), nvDict.keys(), nvDict.values()))
    return list_info

def main():
    info_result = []
    page =1
    while page < 10:
        info_list = get_result(page)
        info_result = info_result + info_list
        page += 1
    # print(info_list)
    # print(info_result)
    for row in info_result:
        d = get_proxies(row[0],int(row[1]))
        print(d)
        daili(d)
        # wb = Workbook()
        # ws1 = wb.active
        # ws1.title = 'ip'
        # for row in info_result:
        #     ws1.append(row)
        # wb.save('ip'+'.xlsx')

if __name__ == '__main__':
    main()
