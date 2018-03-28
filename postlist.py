#!/usr/bin/python3
import hashlib
import configparser
import sqlite3
import datetime
from flask import Flask, render_template, request, Response
from functools import wraps

app = Flask(__name__)      

Config = configparser.ConfigParser()
Config.read("postlist.conf")


def dbconnect():
    try:
        db = Config['Main']['Database']
    except:
        print("Config Error!")
        exit()
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    if(('headers',) not in tables): 
        cur.execute('''CREATE TABLE headers
                        (name text);''')

    if(('logs',) not in tables): 
        cur.execute('''CREATE TABLE logs
                        (contents TEXT,
                        date TEXT);''')

    if(('accounts',) not in tables):
        cur.execute('''CREATE TABLE accounts
                        (username TEXT,
                        password TEXT);''')

        print("Create a master user.")
        username = input("Username: ")
        password = input("Password: ")
        password = hashlib.sha256(str(password).encode()).hexdigest()
        cur.execute("INSERT INTO accounts VALUES(?, ?)",(username, password))

    conn.commit()
    return conn,cur

def dbclose(conn):
    conn.close()

def load_namelist():
    conn,cur = dbconnect()
    cur.execute("SELECT name FROM headers;")
    name_list = []
    headers = cur.fetchall()
    print(headers)
    for header in headers:
        namelist.append(header[0])
    dbclose(conn)
    return name_list

def check_auth(username, password):
    conn,cur = dbconnect()
    cur.execute("SELECT password FROM accounts WHERE username=?",(username,))
    db_pass = cur.fetchone()
    dbclose(conn)
    if db_pass !=None:
        return password == db_pass[0]
    else:
        return False

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, hashlib.sha256(str(auth.password).encode()).hexdigest()):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/postlist',methods=["POST","GET"])
#@requires_auth
def home():
    name_list = load_namelist()
    if request.method == "POST":
        ln = request.form.keys()
        for item in ln:
            if item == 'submit':
                print(end='')    
            elif item == 'action':
                data = []
                conn,cur = dbconnect()
                cur.execute("SELECT content FROM logs;")
                for log in cur.fetchall():
                    data.append(log[0])
                dbclose(conn)
                return render_template('home.html',names=name_list,ip="/postlist",dats=data)
                        
    return render_template('home.html',names=name_list,ip="/postlist",dats=[])

@app.route('/postlist/data',methods=["POST"])
#@requires_auth
def data():
    name_list = load_namelist()
    ln = request.form.keys()
    conn,cur = dbconnect()
    print(ln)
    for item in ln:
        print(item)
        if item not in name_list:
            name_list.append(item)
            cur.execute("INSERT INTO headers VALUES(?);",item)
            cur.execute("INSERT INTO logs VALUES(?,?);",request.form[item],datetime.datetime.now())
        else:
            cur.execute("INSERT INTO logs VALUES(?,?);",request.form[item],datetime.datetime.now())
    conn.commit()
    dbclose(conn)
    return render_template('blank.html')

if __name__ == '__main__':
    conn,cur = dbconnect()
    dbclose(conn)
    app.run(host='0.0.0.0', port=5000)
