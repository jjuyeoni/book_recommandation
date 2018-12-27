from book.models import *

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd
import re
# import html5lib
# from django.http import HttpResponse
import urllib.parse

# bestseller crawling
def bestSeller():
    title = []
    author_info = []
    href = []
    img_path = []

    url = "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?orderClick=d79"
    html = urlopen(url)
    soup = bs(html, "html.parser")
    tmp = soup.find_all('ul', 'list_type01')[0]

    i = 0

    while i < 12:
        for t in tmp.find_all('li'):
            img = t.find('div', 'cover')
            if (img != None):
                img_path.append(img.find('img')['src'])
                title.append(t.find(class_="title").find('strong').get_text())
                href.append(t.find(class_="title").get('href'))
                a = t.find(class_="author").get_text().split()
                author_info.append(a)
                i += 1

    data = {'Title': title, 'Author_info': author_info, 'img_path': img_path}
    df = pd.DataFrame(data)
    df = df.reset_index()
    return df

#강남구 도서관
def gangnam(title):
    url1 = "http://library.gangnam.go.kr/search/tot/result?q="
    url2 = urllib.parse.quote_plus(title)
    url3 = "&st=EXCT&si=TOTAL&oi=&os=&cpp=50"

    pageurl = url1+url2+url3
    Url = urlopen(pageurl)
    soup1 = bs(Url, "html.parser")

    g_library = soup1.select("dd.bookline.locCursor > span")

    liblist_list =[]
    liblist = {
        'libname':'',
        'libstatus':'',
    }
    if (g_library==[]):

         liblist = {
             'libname' : '소장 도서관이 없습니다',
             'libstatus' : ' '
             }
         liblist_list.append(liblist)


    else :
            for library in g_library:
                        libname = library.contents[0]
                        libstatus = library.contents[1].text
                        liblist = {
                                'libname' : libname,
                                'libstatus' : libstatus
                                }
                        liblist_list.append(liblist)
    return liblist_list
