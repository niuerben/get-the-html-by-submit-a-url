import sys
from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import sqlite3

def main():

    baseurl = input("please submit a url, eg:https://www.baidu.com/. 请输入一条链接")
    datalist = getData(baseurl,baseurl)


def getData(baseurl,url):
    html = askURL(url)
    print(html)


def askURL(url):
    head={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
    }

    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


if __name__ == '__main__':
    main()
    print("爬取完毕!")
