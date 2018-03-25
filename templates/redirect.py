#!/usr/bin/python3
import hashlib
from flask import Flask, render_template, request, Response
from functools import wraps

app = Flask(__name__)      

@app.route('/',methods=["GET"])
def redir():
    return render_template('redirect.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
