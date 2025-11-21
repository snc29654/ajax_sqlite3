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

import re
import sys
import bs4
import requests
from urllib.parse import urljoin
dbname = '../ajax_sqlite3.db'

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

zip_code=[]

def get_link(url):
    # ページ取得
    res = requests.get(url)
    res.raise_for_status()

    # リンク取得
    soup = bs4.BeautifulSoup(res.text, "lxml")
    links = soup.select("a")

    keys = set()
    results = []
    for link in links:
        # リンクURL取得
        link_url = link.get("href")
        if not link_url:
            continue

        # URL補完
        if not link_url.startswith("http"):
            link_url = urljoin(url, link_url)

        # リンクテキスト取得
        link_text = link.text
        if not link_text:
            link_text = ""
        link_text = link_text.strip()
        link_text = re.sub(r"\n", " ", link_text)

        # 重複削除
        key = link_url + link_text
        if key in keys:
            continue
        keys.add(key)

        results.append({"url": link_url, "text": link_text})

    return results


def copy_link(url):
    # リンク取得
    results = get_link(url)

    text = ""
    for result in results:
        text +=  "<a href= \"" + result["url"] + "\"</a>"+result["text"] + "\t" +"<br>" +"\n"   

        text +=  "<a>"   

        text+=" <input value=\"scrape\" style=\"background-color:gray\" onclick=\"func_news_next("
        text+=repr(result["url"])
        text+=","
        text+=repr(result["text"])
        text+=")  \"  type=\"button\"></input>"

        text +=  "</a>"   
        text +=  "<a>"

        text+=" <input value=\"next\" style=\"background-color:gray\" onclick=\"func_list_next("
        text+=repr(result["url"])
        text+=","
        text+=repr(result["text"])
        text+=")  \"  type=\"button\"></input>"

        text +=  "</a>"


    return(text)



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

    r = requests.get(url)

    data = BeautifulSoup(r.content, 'html.parser')
    find_data=data.find_all("a")
    return(find_data)



cgitb.enable()
form=cgi.FieldStorage()
zip_code=form.getvalue("sent2")

find_data=copy_link(zip_code)

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
    c.executemany(insert_sql, users)
    conn.commit()

print("Content-type: text/html\n")

print(find_data)
