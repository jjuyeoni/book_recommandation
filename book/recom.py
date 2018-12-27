
# kakao 책검색
def get_book_info(q) :
    url = "https://dapi.kakao.com/v3/search/book?target=title&query="+q
    headers = {'Authorization': 'KakaoAK {}'.format('f86dda3153f74c45aca17bcedb68987b')}

    try:
        res = requests.get(url, headers=headers)
        return res.json()
    except Exception as e:
        print(str(e))
        sys.exit(0)

# tf-idf
def tfidfvectorizerContents(data, max_dfv=0.8,max_featuresv=1000,min_dfv=0.02 ):

    eng_stop_words = list(set(stopwords.words('english')))
    book_stop_words = ['class', '영역', '시작', '분야상세보기' ,'배너' ,'gif', 'src','img','하위','http' , 'href', 'sysimage', '상품', '카테고리','alt','bl_arr','blank','height','width','정보', 'image', 'alt', 'morecate', 'renew','더보기','교환','빠른분야', 'com','bl_arrr','dvd', '비주얼','반품','안내','관련','행사','body','분야','보기','도서','메뉴','상세','중고','할인','공연','영화','도서','배송','판매','가격','포인트','구입','예매','상세','소개','이미지','레이어','문의','광고','예스','패션','이벤트','국내','연재','어린이','음반','서비스','리뷰','소비자','키즈','해외','코너','쿠폰','플래티넘','로얄','골드','제휴','페이지','외국','해외','추가','경우','만원','바로가기','페이지','비주','플레티넘','오버레이','링크','블루레이','평일','공휴일','기간','스크립트','회원','그림','텍스트','버튼','헤더','품절','마이','수입','센터','메일','수량','이상','한정','취소','적립','다운로드','카트','검색','주문','채널','센터','구매','고객','마케팅','바로','해더','제목','사이트','세부','환불','휴무','배송비','vol','code','footer','script','tracking','거래처']
    stop_words = eng_stop_words + book_stop_words
    tfidf_vectorizer = TfidfVectorizer(max_df=max_dfv, max_features=max_featuresv, min_df=min_dfv, stop_words=stop_words,use_idf=True, ngram_range=(1,1),dtype=np.int64)

    # 한국어 형태소 분석기( KoNlpy )
    twitter = Twitter()

    corpus = []
    glued_list = ['author_intro', 'cats', 'maker_review', 'more_contents', 'og:description', 'og:title']
    for i in range(len(bookList)):
        document = ''
        try :
            k = data.loc[i]
            last_c = None
            last_record = k
            for j in glued_list:
                if k[j] != None:
                    document += " " + str(k[j])
            if(len(document) < 100):
                print('Document Length not over 100 charater', document)
            corpus.append(" ".join(twitter.nouns(document)))
        except :
            print('Parse & iteration error ' , sys.exc_info())
            print(last_c)
            print(last_record)
            sys.exit()

    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
    indices = np.argsort(tfidf_vectorizer.idf_)[::-1]
    features = tfidf_vectorizer.get_feature_names()

    return tfidf_matrix

#유사도 분석 함수
def similar_recommend_by_content(booklens_id):
    result = []
    # s = np.load('book/matrix/story_matrix.npy')
    # s = np.asmatrix(s)
    tfidf_matrix = tfidfvectorizerContents(bookList)
    book_sim = cosine_similarity(tfidf_matrix)

    book_index = booklens_id
    similar_books = sorted(list(enumerate(book_sim[book_index])),key=lambda x:x[1], reverse=True)
    recommended=1

    for book_info in similar_books[1:5]:
        recommended+=1
        result.append(book_info[0])
    return result
