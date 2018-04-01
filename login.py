import flask_login
import sqlite3
login_manager = flask_login.LoginManager()
@login_manager.user_loader
def load_user(user_id):
   print() 
