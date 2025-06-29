from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
import os
import pymysql
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime


user_app = Blueprint('login', __name__)



#업로드 폴더 설정
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png','jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#mysql 연결
from db import db

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

@user_app.route('/')
@user_app.route('/home')
def home():
    return render_template('index.html') 

#회원가입은 GET은 홈페이지 보여주고 POST는 제출 데이터 처리
@user_app.route('/user_register', methods=['GET', 'POST'])
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
            photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], photo_filename))

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

        return redirect(url_for('login.login'))

    return render_template('user_register.html')

@user_app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_id = request.form['login_id']
        password = request.form['password']

        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE login_id = %s", (login_id,))
            user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            #로그인 성공하면 flask 세션에 사용자 정보 저장해서 로그인 상태 유지지
            session['user_id'] = user['id']
            session['login_id'] = user['login_id']
            session['name'] = user['name']
            return redirect(url_for('login.home'))
        else:
            #로그인 실패
            #flash 메세지 
            flash("ID 또는 비밀번호가 틀렸습니다.")
            return redirect(url_for('login.login'))

    return render_template('user_login.html') 

@user_app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.home'))

@user_app.route('/mypage')
def mypage():
    #로그인 안 되어 있으면 로그인 창으로 
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    user_id = session['user_id'] #현재 로그인 사용자 ID
    search = request.args.get('search', '') #검색창에 입력된 문자열 받기
    like_pattern = f"%{search}%" #sql의 LIKE 문으로 바꿔줌 

    with db.cursor() as cursor:
        # 로그인한 사용자 전체정보 가져오기
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        # 친구 목록 가져오기 (검색 조건 여부에 따라 다르게)
        if search: #검색어 있는 경우 
            sql = """
                SELECT DISTINCT u.id, u.name, u.login_id, u.mbti
                FROM friends f
                JOIN users u
                  ON (
                      (u.id = f.friend_id AND u.login_id = %s)
                      OR (u.id = u.login_id AND f.friend_id = %s)
                )
                WHERE f.status = 'accepted'
                  AND u.id != %s
                  AND (
                      u.name LIKE %s OR
                      u.login_id LIKE %s OR
                      u.mbti LIKE %s
                  )
            """
            cursor.execute(sql, (user_id, user_id, user_id, like_pattern, like_pattern, like_pattern))
        else: #검색어 없을 
            sql = """
                SELECT DISTINCT u.id, u.name, u.login_id, u.mbti
                FROM friends f
                JOIN users u
                  ON (
                      (u.id = f.friend_id AND f.user_id = %s)
                      OR (u.id = f.user_id AND f.friend_id = %s)
                  )
                WHERE f.status = 'accepted' AND u.id != %s
            """
            cursor.execute(sql, (user_id, user_id, user_id))

        friends = cursor.fetchall()
        friend_count = len(friends)

    return render_template('mypage.html', user=user, friends=friends, friend_count=friend_count)

@user_app.route('/user_update', methods=['GET', 'POST'])
def user_update():
    #로그인 안 되어있으면 login 페이지로 
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    #로그인한 사용자 id user_id에 저장
    user_id = session['user_id']

    #post일 때 기존 정보 수정함. 
    if request.method == 'POST':
        name = request.form['name']
        mbti = request.form['mbti']
        email = request.form['email']
        birth = request.form['birth']
        address = request.form['address']
        introduction = request.form['introduction']
        new_password = request.form.get('password')
        photo = request.files.get('photo')

        # 사용자 기본 정보 수정
        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE users
                SET name=%s, mbti=%s, email=%s, birth=%s,
                    address=%s, introduction=%s
                WHERE id=%s
            """, (name, mbti, email, birth or None, address, introduction, user_id))
            db.commit()

        # 비밀번호 수정 (입력된 경우에만)
        if new_password:
            hashed_pw = generate_password_hash(new_password)
            with db.cursor() as cursor:
                cursor.execute("UPDATE users SET password=%s WHERE id=%s", (hashed_pw, user_id))
                db.commit()

        # 프로필 사진 수정 (파일이 선택된 경우에만)
        if photo and photo.filename:
            photo_filename = secure_filename(photo.filename)
            photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], photo_filename))
            with db.cursor() as cursor:
                cursor.execute("UPDATE users SET photo_filename=%s WHERE id=%s", (photo_filename, user_id))
                db.commit()

        return redirect(url_for('login.mypage'))

    # GET 요청: 사용자 정보 불러오기
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

    return render_template('user_update.html', user=user)

@user_app.route('/delete_user', methods=['POST'])
def delete_user():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))  # 경로도 user_login으로 수정

    user_id = session['user_id']

    with db.cursor() as cursor:
        # 먼저 친구 관계 전부 삭제 (요청자거나 수락자인 경우 모두)
        cursor.execute("DELETE FROM friends WHERE user_id = %s OR friend_id = %s", (user_id, user_id))
        # 그 다음 사용자 삭제제
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db.commit()

    session.clear()
    return redirect(url_for('login.home'))


if __name__ == '__main__':
    app.run(debug=True)
