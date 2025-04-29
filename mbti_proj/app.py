from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector

friend_bp = Blueprint('friend', __name__)
db = mysql.connector.connect(
    host="localhost", 
    user="flaskuser",  # mysql 새사용자 생성->flaskuser
    password="1234", 
    database="mbti_db")

cursor = db.cursor(dictionary=True) # 데이터 dict 형태로 전달
CURRENT_USER_ID = 1

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html') 

@app.route('/home')
def home():
    return render_template('home.html') 

@app.route('/user_register')
def user_register():
    return render_template('user_register.html') 

@app.route('/user_login')
def user_login():
    return render_template('user_login.html') 
if __name__ == '__main__':
    app.run(debug = True)