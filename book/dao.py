from django.db import connection
import pandas as pd

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
    print(df['publisher'][0])
    query_string = "INSERT INTO `mysite`.`book_data` (`authors`,`corp`,`description`,`image`,`title`,`url`) VALUES (\'" + df['authors'][0] + "\', \'"+ df['publisher'][0] + "\', \'"+df['contents'][0]+ "\', \'"+df['thumbnail'][0]+ "\', \'"+df['title'][0]+ "\', \'"+df['url'][0]+"\');"
    cursor.execute(query_string)
    return cursor.lastrowid

def selectBookAll():
    cursor = connection.cursor()
    query_string = "SELECT * FROM book_data;"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    book=[]
    for row in rows :
        book.append({'id':row[0], 'author_intro':row[2], 'cats':row[6], 'maker_review':row[8], 'more_contents':row[9], 'description':row[10], 'title':row[13], 'url':row[14]})
    d = pd.DataFrame(book)
    return d

def wordcloudById(id):
    book = ""
    cursor = connection.cursor()
    query_string = "SELECT * FROM book_data where id = \'" + id + "\';"
    cursor.execute(query_string)
    rows = cursor.fetchall()
    for row in rows :
        book = row[5] + row[6] + row[8] + row[10]
    return str(book)
