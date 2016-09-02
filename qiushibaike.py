# -*- coding: UTF-8 -*-
import requests
from openpyxl import Workbook
from lxml import etree

def get_qiushi(page):
    html = requests.get('http://www.qiushibaike.com/hot/page/'+str(page),headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
})
    title_list = []
    qiushi_list = []
    selector = etree.HTML(html.text)
    #print(html.text)
    title = selector.xpath('.//*[@class="author clearfix"]/a[2]/h2/text()')
    qiushi = selector.xpath('.//*[@class="content"]/text()')
    for each in title:
        title_list.append(each)
    for each in qiushi:
        qiushi_list.append(each)

    nvs = zip(title_list, qiushi_list)
    nvDict = dict((name, value) for name, value in nvs)

    list_info = list(map(lambda x, y: (x, y), nvDict.keys(), nvDict.values()))
    return list_info

def main():
    info_result = []
    page = 0
    pages = input('你想看几页？一页20条哦：')
    while page < int(pages):
        info_list = get_qiushi(pages)
        info_result = info_result + info_list
        page += 1
    #print(info_list)
    wb = Workbook()
    ws1 = wb.active
    ws1.title = pages+'页糗事百科'
    for row in info_result:
        ws1.append(row)
    wb.save(pages+'页糗事百科'+'.xlsx')

if __name__ == '__main__':
    main()
