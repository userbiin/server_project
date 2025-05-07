from flask import Flask, render_template, request, redirect, url_for
import os
import pymysql
from werkzeug.security import generate_password_hash
from datetime import datetime

#Flask객체 생성
app = Flask(__name__)

#업로드 폴더 설정
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#mysql 연결
db = pymysql.connect(
    host='127.0.0.1',  #codespace환경에서 TCP연결임
    user='flaskuser',
    password='1234',
    database='mbti_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

#테이블 생성
def create_users_table():
    with db.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                login_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                birth DATE,
                mbti VARCHAR(4),
                address TEXT,
                introduction TEXT,
                photo_filename VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    db.commit()

create_users_table()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html') 

#회원가입은 GET은 홈페이지 보여주고 POST는 제출 데이터 처리
@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST' :
        login_id = request.form['login_id']
        name = request.form['name']
        mbti = request.form['mbti']
        birth = request.form['birth']
        email = request.form['email']
        address = request.form['address']
        introduction = request.form['introduction']
        password = request.form['password']
        photo = request.files['photo']

        #비밀번호 해싱 
        hashed_pw = generate_password_hash(password)

        #프로필 사진 저장 
        photo_filename = ''
        if photo and photo.filename != '':
            photo_filename = photo.filename
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        #insert query
        with db.cursor() as cursor:
            sql = """
                INSERT INTO users
                (login_id, name, email, password, birth, mbti, address, introduction, photo_filename)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql,(
                login_id, name,email,hashed_pw, birth or None, mbti,
                address, introduction, photo_filename
            ))

        db.commit()

        return redirect(url_for('home'))

    return render_template('user_register.html')

@app.route('/user_login')
def user_login():
    return render_template('user_login.html') 

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port=5000)