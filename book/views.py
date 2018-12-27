from django.shortcuts import render, redirect
from . import dao
from book.models import *
from django.conf import settings
from . import crawler
from . import recom
import pandas as pd

#####
#from wordcloud import WordCloud, STOPWORDS
#from konlpy.tag import Twitter; t = Twitter()
#import nltk
#import matplotlib.pyplot as plt
#import sys
#from PIL import Image
#import os
#####

#Wordcloud용 크롤러
# def parseContentLike(url):
#     try :
#         html = urlopen(url)
#         htmldata = html.read()
#         b = bs(htmldata, 'html5lib')
#         fb_metas = b.find_all('meta', attrs={'property':True})
#         cats = b.select('.basicListType ul li a')
#         author_trl = b.select('span.gd_auth a')
#         pub_corp = b.select('span.gd_pub a')
#         pub_date = b.select('span.gd_date')
#         pub_ori_title = b.select('span.gd_origin a')
#         book_cont = {}
#         prd_sdata =  b.select('#contents .basicListType td.cell_2col')
#         cm = b.select('div.communtyHide')
#     except :
#         print('Unexpected Error ', sys.exc_info())
#         return False;
#     bdata = ''
#     if b.find('a',attrs={'name':'contentsIntro'}) != None:
#         t_cnt = 0
#         for tag in b.find('a',attrs={'name':'contentsIntro'}).next_elements:
#             t_cnt +=1
#             if(t_cnt==2):
#                 book_intro = re.sub(r'(\n|\s\s)','',tag.text.strip())
#                 break
#     else :
#         book_intro = " "
#     bdata += " " + book_intro
#     return bdata

#Wordcloud함수

#def Cloud(uid, fname):
#    b_id = udao.selectBlike(uid)
#    print("bid", b_id)
#    bList=[]
#    for i in b_id:
#        bList.append(dao.selectTitleBook(i))
#    data =''
#    print("blist", bList[0])
#    for b in bList:
#        data += " " + parseContentLike(b)
#    mask = np.array(Image.open("book/static/img/book_bg.jpg"))
#    tokens_ko = t.nouns(data)
#    ko = nltk.Text(tokens_ko, name='wcc')
#    stop_words = ['.', '(', ')', ',', "'", '%', '-', 'X', ').', '×','의','자','에','안','번','호','을','이','다','만','로','가',
#    '를','나','그', '이다', '준', '이', '것', '호', '과연', '수', '게', '개', '설', '때', '책', '주로', '저자', '작가', '더', '도', '듯', '반', '왜', '줄','고',
#    '봐', '천', '뭐', '때문','함', '세']
#    ko = [each_word for each_word in ko if each_word not in stop_words]
#    ko = nltk.Text(ko, name='wcc')
#    data = ko.vocab().most_common(100)
#    wordcloud = WordCloud(font_path='book/NotoSansKR-Regular.otf',relative_scaling = 0.2,background_color='white',mask=mask,margin=7,).generate_from_frequencies(dict(data))
#    plt.figure(figsize=(12,8))
#    plt.imshow(wordcloud)
#    plt.axis("off")
#    fig1 = plt.gcf()
#    name = "book"+ str(fname)
#    fig1.savefig(name, dpi=100)


# Create your views here.
def book_list(request):
    df = crawler.bestSeller()
    bookList=[]
    for i in range(0, 12) :
        a = {'index':df['index'][i] + 1, 'Title':df['Title'][i], 'Author':df['Author_info'][i],'img_path':df['img_path'][i]}
        bookList.append(a)
    return render(request, 'book/book_list.html', {'bookList':bookList})

def search(request):
    if request.method == 'POST' :
        title = request.POST['title']
        bookid = dao.selectBook(title)
        if bookid == False :
            bookIDDF = recom.get_book_info('title')
            bookIDDF = pd.DataFrame(bookIDDF['documents'][0])

            bookid = dao.insertNewBook(bookIDDF)

            # return render(request, 'book/error.html')
        bookList = dao.selectBookAll()
        # bookList = pd.DataFrame(bookList)
        recom_book = recom.similar_recommend(bookid, bookList)

        recom_result = []
        for i in recom_book:
            recom_result.append(dao.selectResultBook(str(i+1)))

        return render(request, 'book/search.html', {'cont':recom_result})

def mybook(request, num):
    check = dao.checkBlike(num, request.user.id)
    if check == 0 :
        b = Blike(u = request.user, b_id = num)
        b.save()
#    l_id = dao.selectLikeId(num)
#    uid = request.user.id
#    name = str(l_id) + '_' + str(uid) + ".png"
#    if l_id > 0:
#        isFile = "book/static/img/" + str(l_id - 1) + '_' + str(uid) + ".png"
#        if os.path.isfile(isFile):
#            os.remove(isFile)
#    fname = "/static/img/" + name
#    Cloud(uid, fname)
    return redirect(b_search)

def detail(request, title):
    data = dao.selectBookbytitle(title)
    ganglist = crawler.gangnam(title)
    check = dao.checkBlike(data['id'], request.user.id)
    return render(request, 'book/detail.html', {'data':data, 'ganglist':ganglist, 'check':check})

#책검색
def b_search(request):
    return render(request, 'book/book_search.html')

def bAjax(request):
    if request.method == 'POST':
        data = request.POST['title']
        return detail(request, data)
    return render(request, 'book/book_search.html', {'time':time})
