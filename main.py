#!/usr/bin/python3
from flask import Flask, render_template, request
 
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
print(name_list)

@app.route('/',methods=["POST","GET"])
def home():
    if request.method == "POST":
        ln = request.form.keys()
        for item in ln:
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
        return render_template('home.html')
            
    if request.method == "GET":
        return render_template('home.html')
 
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)
