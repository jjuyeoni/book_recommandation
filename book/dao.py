from django.db import connection

def selectBook(title):
    cursor = connection.cursor()
    query_string = "SELECT id FROM book_data where title = \'" + title + "\';"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    if not rows :
        return False;
    book = rows[0]
    return book

def selectBookbytitle(title):
    cursor = connection.cursor()
    query_string = "SELECT * FROM book_data where title = \'" + title + "\';"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    for row in rows :
        book = {'id':row[0], 'author_intro':row[2], 'authors':row[3], 'bibli':row[4], 'book_intro':row[5], 'cats':row[6], 'corp':row[7],
        'maker_review':row[8], 'description':row[10], 'image':row[11], 'url':row[14]}
    return book

def selectBookbyid(id):
    cursor = connection.cursor()
    query_string = "SELECT * FROM book_data where id = \'" + id + "\';"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    for row in rows :
        book = {'id':row[0] , 'image':row[11], 'title':row[13], 'url':row[14]}
    return book

def selectResultBook(id):
    cursor = connection.cursor()
    query_string = "SELECT * FROM book_data where id = \'" + id + "\';"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    for row in rows :
        book = {'image':row[11], 'title':row[13]}
    return book

def selectSearchBook(title):
    cursor = connection.cursor()
    k = '%' + title + '%'
    query_string = "SELECT title FROM book_data where title LIKE \'" + k + "\';"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    book = []
    for row in rows :
        book.append(row[0])
    return book

def checkBlike(b_id, u_id):
    cursor = connection.cursor()
    query_string = "select count(*) from book_blike where u_id = \'" + str(u_id) + "\' and b_id= \'" + str(b_id) + "\';"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    for row in rows :
        check = row[0]
    return check

def selectLikeId(b_id):
    cursor = connection.cursor()
    query_string = "SELECT id FROM book_blike where b_id = \'" + b_id + "\';"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    for row in rows :
        l_ib = row[0]
    return l_ib

def selectTitleBook(id):
    cursor = connection.cursor()
    query_string = "SELECT url FROM book_data where id = \'" + id + "\';"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    for row in rows :
        book = row[0]
    return book

def insertNewBook(df):
    cursor = connection.cursor()
    query_string = "INSERT INTO book_data('authors','corp','description','image','url') VALUES (%s, %s, %s, %s, %s)"
    val = (df['authors'],df['publisher'],df['contents'],df['thumbnail'],df['url'])
    cursor.execute(query_string, val)
    cursor.commit()
    return cursor.lastrowid

def selectBookAll():
    cursor = connection.cursor()
    query_string = "SELECT * FROM book_data;"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    for row in rows :
        book = {'id':row[0], 'author_intro':row[2], 'authors':row[3], 'bibli':row[4], 'book_intro':row[5], 'cats':row[6], 'corp':row[7],
        'maker_review':row[8], 'description':row[10], 'image':row[11], 'url':row[14]}
    return book
