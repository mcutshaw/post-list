#!/usr/bin/python3
import hashlib
import configparser
import sqlite3

def dbconnect():
    try:
        Config = configparser.ConfigParser()
        Config.read("postlist.conf")
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
                        (header TEXT,
                        contents TEXT,
                        date TEXT);''')

    if(('accounts',) not in tables):
        cur.execute('''CREATE TABLE accounts
                        (username TEXT,
                        password TEXT,
                        role TEXT,
                        logs TEXT);''')

        print("Create a master user.")
        username = input("Username: ")
        password = input("Password: ")
        password = hashlib.sha256(str(password).encode()).hexdigest()
        cur.execute("INSERT INTO accounts VALUES(?, ?, 'all', 'all')",(username, password))

    conn.commit()
    return conn,cur

def dbclose(conn):
    conn.close()

def new_user(username,password,role,logs):
    conn,cur = dbconnect()
    cur.execute("INSERT INTO accounts VALUES(?, ?, ?, ?)",(username, hashlib.sha256(str(password).encode()).hexdigest(), role, logs))
    conn.commit()
    dbclose(conn)

def load_namelist():
    conn,cur = dbconnect()
    cur.execute("SELECT name FROM headers;")
    name_list = []
    headers = cur.fetchall()
    print(headers)
    for header in headers:
        name_list.append(header[0])
    dbclose(conn)
    return name_list

def load_userlist():
    conn,cur = dbconnect()
    cur.execute("SELECT username,password,role,logs FROM accounts;")
    user_list = []
    users = cur.fetchall()
    for user in users:
        user_list.append(user)
    dbclose(conn)
    return user_list
