import cgi
import cgitb
import json
import sys
import io
import requests
from bs4 import BeautifulSoup
import sqlite3
from contextlib import closing
import datetime

dbname = '../ajax_sqlite3.db'

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

zip_code=[]

def  data_print(url):
    global zip_code

    params = {'p':zip_code,
          'search.x':'1',
          'fr':'top_ga1_sa',
          'tid':'top_ga1_sa',
          'ei':'UTF-8',
          'aq':'',
          'oq':'',
          'afs':'',}

    r = requests.get(url, params=params)

    data = BeautifulSoup(r.content, 'html.parser')
    return(data)



cgitb.enable()
form=cgi.FieldStorage()
zip_code=form.getvalue("sent2")

find_data=data_print("http://search.yahoo.co.jp/search")

date = datetime.date.today()

name=""
weather=""
kind=""

with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()
    create_table = '''create table users (id INTEGER PRIMARY KEY,date varchar(64), name varchar(64),
                      weather varchar(64), kind varchar(32), zip_code varchar(64),Contents varchar(256))'''
    try:
        c.execute(create_table)
    except:
        print("database already exist")
        
    scraping_contents=find_data
    Contents = str(scraping_contents)
    insert_sql = 'insert into users (date, name, weather, kind, zip_code,Contents) values (?,?,?,?,?,?)'
    users = [
    (date, name, weather, kind, zip_code,Contents)
    ]
    #c.executemany(insert_sql, users)
    find_data=[]
    
    select_sql = 'select * from users'
    try:
        for row in c.execute(select_sql):
            find_data.append(row)
    except:
        print("data not found")

    conn.commit()

print("Content-type: text/html\n")





print(find_data)
