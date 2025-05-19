from flask import Blueprint, render_template, request, redirect, url_for, session
import time, os, uuid #이미지 고유성 보장
import pymysql
from werkzeug.utils import secure_filename  # 한글 등 위험 문자 대체

feed_bp = Blueprint('feed', __name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 폴더 없으면 자동생성 해줌.


db = pymysql.connect(host='localhost', user='flaskuser', password='1234', db='mbti_db', charset='utf8')
cursor = db.cursor()

@feed_bp.route('/myFeed', methods=['GET', 'POST'])
def feed():
    if 'login_id' not in session:
        return redirect(url_for('login.login'))

    CURRENT_USER_ID = session['login_id'] #현재 로그인 사용자 ID
    if (request.method == 'GET'):
        # user_id에 해당하는 피드 테이블 불러오기
        cursor.execute("SELECT * FROM feeds WHERE user_id=%s", (CURRENT_USER_ID,))
        table = cursor.fetchall()

        # html에 게시글 순서 리스트, 테이블 데이터 전달
        return render_template('myFeed.html', table=table)

    elif (request.method == 'POST'):
        action = request.form.get("action")
        if action == "upload":
            # 클라이언트에서 보낸 데이터 저장
            upload_comment = request.form['upload_comment']
            upload_file = request.files.get('upload_file')  # 없으면 None으로 저장

            file_path = None
            if upload_file and upload_file.filename != '':
                orig_filename = upload_file.filename
                safe_filename = secure_filename(orig_filename)
                ext = os.path.splitext(safe_filename)[1]  # 확장자 추출
                final_filename = str(int(time.time())) + '_' + str(uuid.uuid4()) + ext
                file_path = os.path.join(UPLOAD_FOLDER, final_filename)  # 파일 경로 합치기
                upload_file.save(file_path)  # 서버 폴더에 upload_file 저장하기
                file_path = file_path.replace('\\', '/')  # 윈도우 경로 슬래시 통일

            cursor.execute("INSERT INTO feeds (user_id, content, file_path) VALUES (%s, %s, %s);", (CURRENT_USER_ID, upload_comment, file_path))

            db.commit()
            return redirect(url_for('feed.feed'))
        elif action == "delete": #피드 게시글 삭제
            delete_id = request.form['delete_id']
            cursor.execute("SELECT file_path FROM feeds WHERE id=%s", (delete_id,))
            file_path = cursor.fetchone()[0]

            if file_path and os.path.exists(file_path):
                os.remove(file_path)

            cursor.execute("DELETE FROM feeds WHERE id=%s", (delete_id,))
            db.commit()
            return redirect(url_for('feed.feed'))


@feed_bp.route('/feedSearch')
def feed_search():
    if 'login_id' not in session:
        return redirect(url_for('login.login'))
    friend_id = request.args.get('friend_id')
    table = []
    if friend_id:
        #먼저 friend_id가 유효한지 확인
        cursor.execute("SELECT EXISTS(SELECT 1 FROM feeds WHERE user_id = %s)", (friend_id,))
        result = cursor.fetchone()[0]
        if result:
            cursor.execute("SELECT * FROM feeds WHERE user_id=%s", (friend_id,))
            table = cursor.fetchall()
        else:
            message = f"ID '{friend_id}'에 해당하는 피드가 없습니다."
            return render_template('feedSearch.html', table=table, message=message)
    return render_template('feedSearch.html', table=table)
