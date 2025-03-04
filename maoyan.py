import sys
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sqlite3

from douban.spider import findImgSrc


def main():
    baseurl = "https://piaofang.maoyan.com/rankings/year"
    datalist = getData(baseurl)
    savepath = "猫眼票房Top100.xls"
    saveData(datalist,savepath)
    askURL("https://piaofang.maoyan.com/rankings/year")

findLink = re.compile(r'href:\'(.*)\'')
findTitle = re.compile(r'<p class="first-line">(.*)</p>')
findImgSrc = re.compile(r'')
findTicket = re.compile(r'<li class="col2 tr">(.*)</li>')
findPrice = re.compile(r'<li class="col3 tr">(.*)</li>')
findAttend = re.compile(r'<li class="col4 tr">(.*)</li>')

# <ul class="row" data-com="hrefTo,href:'/movie/1294273'">
# <li class="col2 tr">票房(万元)</li>
# <li class="col3 tr">平均票价</li>
# <li class="col4 tr">场均人次</li>

def getData(baseurl):
    datalist = []

    url = baseurl
    html = askURL(url)

    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    i = 0
    for item in soup.find_all('ul', class_="row"):
        print(item)    #测试

        if i == 0:
            i += 1
            continue

        item = str(item)
        data = []

        titles = re.findall(findTitle, item)
        ctitle = titles[0]
        data.append(ctitle)

        link = re.findall(findLink, item)[0]        #链接
        # data.append(link)
        imgSrc = "https://piaofang.maoyan.com"  # 图片
        imgSrc += link
        data.append(imgSrc)

        ticket = re.findall(findTicket, item)[0]    #票房
        data.append(ticket)

        price = re.findall(findPrice, item)[0]      #平均票价
        data.append(price)

        attend = re.findall(findAttend,item)[0]     #场均人次
        data.append(attend)

        datalist.append(data)

    print(datalist)
    return datalist


def saveData(datalist, savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8",style_compression = 0)      # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)     #创建工作表
    col =("片名","图片链接","票房","平均票价","场均人次")
    for i in range(0,5):
        sheet.write(0,i,col[i])  # 列名

    for i in range(0,100):
        print("第 %d 条"%(i+1))
        data = datalist[i]
        for j in range(0, 5):
            sheet.write(i + 1,j, data[j])
        # 数据
    book.save(savepath)    # 保存

def askURL(url):
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


if __name__ == '__main__':
    main()
    print("爬取完毕!")