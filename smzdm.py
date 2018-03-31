# -*- coding: UTF-8 -*-
import requests
from openpyxl import Workbook
from lxml import etree

def get_result(searchName,page):
    html = requests.post('http://search.smzdm.com/?c=home&s='+searchName+'&p='+str(page),headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
})
    title_list = []
    price_list = []
    selector = etree.HTML(html.text)
    title = selector.xpath('.//*[@class="feed-nowrap"]/@title')
    price = selector.xpath('.//*[@class="z-highlight"]/text()')
    for each in title:
        title_list.append(each)
    for each in price:
        price_list.append(each)

    nvs = zip(title_list, price_list)
    nvDict = dict((name, value) for name, value in nvs)

    list_info = list(map(lambda x, y: (x, y), nvDict.keys(), nvDict.values()))
    return list_info

def main():
    searchName = input('搜索关键字： ')
    info_result = []
    page =1
    while page < 4:
        info_list = get_result(searchName,page)
        info_result = info_result + info_list
        page += 1
    print(info_list)
    wb = Workbook()
    ws1 = wb.active
    ws1.title = searchName
    for row in info_result:
        ws1.append(row)
    wb.save(searchName+'.xlsx')

if __name__ == '__main__':
    main()
