#
#pythonでのsqlite3の書き込みです。
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import signal
import sqlite3
from contextlib import closing
dbname = 'ajax_sqlite3.db'

#mainで定義されており  javascriptから受信したら実行されます
def hello_world(request):
    print(request.params)
    in_data=request.params
    passward=in_data["passward"]
    userid=in_data["userid"]
    age=in_data["age"]
    gender=in_data["gender"]
    print(userid)
    print(passward)   
    print(age)   
    print(gender)   
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        create_table = '''create table users (userid varchar(64), name varchar(64),
                      age varchar(64), gender varchar(32))'''
        #登録済でエラーしないようにごまかします
        try:
            c.execute(create_table)
        except:
            print("database already exist")
        insert_sql = 'insert into users (userid, name, age, gender) values (?,?,?,?)'
        users = [
        (userid, passward, age, gender)
        ]
        c.executemany(insert_sql, users)
        conn.commit()
        select_sql = 'select * from users'
        for row in c.execute(select_sql):
            print(row)
   
    return Response("complete" )
    #実行処理  python サーバーを立てています
   
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello',renderer="json")
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()