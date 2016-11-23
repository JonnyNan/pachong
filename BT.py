# -*- coding: UTF-8 -*-
import requests
from openpyxl import Workbook
from lxml import etree

def get_result(searchName,page):
    url = 'http://www.btany.com/search/' + searchName + '-first-asc-' + str(page)
    print(url)
    html = requests.get(url,headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/50.0'
})
    title_list = []
    cili_list = []
    selector = etree.HTML(html.text)
    print(html.headers['content-type'])
    print(html.encoding)
    print(html.apparent_encoding)
    print(requests.utils.get_encodings_from_content(html.text))

    cili = selector.xpath('.//*[@id="wall"]/div/div[3]/a[1]/@href')
    title = selector.xpath('.//*[@id="wall"]/div/div[2]/p/text()')
    for each in title:
        title_list.append(searchName+each)
    for each in cili:
        cili_list.append(each)

    nvs = zip(title_list, cili_list)
    nvDict = dict((name, value) for name, value in nvs)

    list_info = list(map(lambda x, y: (x, y), nvDict.keys(), nvDict.values()))
    return list_info

def main():
    searchName = input('搜索关键字：')
    info_result = []
    page =1
    while page < 3:
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
