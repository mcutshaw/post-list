#!/usr/bin/python3
import hashlib
from flask import Flask, render_template, request, Response
from functools import wraps

app = Flask(__name__)      

name_list = []
name = None
fp = open('logs/names','r')
while name != '':
    name = fp.readline().replace('\n','')
    if name == '':
        break
    name_list.append(name)
fp.close()

def check_auth(username, password):
    fp = open('post-list.conf','r')
    correct_password = fp.read().replace('\n','')
    fp.close()
    return username == 'admin' and password == correct_password

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

@app.route('/',methods=["POST","GET"])
@requires_auth
def home():
    if request.method == "POST":
        ln = request.form.keys()
        for item in ln:
            if item == 'submit':
                print(end='')    
            elif item == 'action':
                fp = open('logs/'+request.form[item].replace('\n',''))
                data = fp.read()
                fp.close()
                data = data.split('\n')
                data.reverse()
                return render_template('home.html',names=name_list,ip="/",dats=data)
                        
    return render_template('home.html',names=name_list,ip="/",dats=[])

@app.route('/data',methods=["POST"])
@requires_auth
def data():
    ln = request.form.keys()
    print(ln)
    for item in ln:
        print(item)
        if item not in name_list:
            name_list.append(item)
            fp = open('logs/names','a')
            fp.write(item+'\n')
            fp.close()
            fp = open('logs/'+item,'w')
            fp.write(request.form[item]+'\n')
            fp.close()
        else:
            fp = open('logs/'+item,'a')
            fp.write(request.form[item]+'\n')
            fp.close()
    return render_template('blank.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc', port=443)
