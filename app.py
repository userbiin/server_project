from flask import Flask, render_template, request, redirect, url_for
import time
import pymysql
import os
import uuid #이미지 고유성 보장
from werkzeug.utils import secure_filename #한글 등 위험 문자 대체

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True) #폴더 없으면 자동생성 해줌.

conn = pymysql.connect(host='127.0.0.1', user='root', password='0000', db='example1_db', charset='utf8')
cur = conn.cursor()
# feed_table 테이블, 테이블 속성은 id, user_id, content, file, time


# user_id는 예시, 나중에 받아와야함.
user_id = "051130"


@app.route('/myFeed', methods=['GET', 'POST'])
def feed():
    if (request.method == 'GET'):
        # user_id에 해당하는 피드 테이블 불러오기
        cur.execute("SELECT * FROM feed_table WHERE user_id=%s", (user_id,))
        table = cur.fetchall()

        # html에 게시글 순서 리스트, 테이블 데이터 전달
        return render_template('myFeed.html', table=table)

    elif (request.method == 'POST'):
        # 클라이언트에서 보낸 데이터 저장
        upload_comment = request.form['upload_comment']
        upload_file = request.files.get('upload_file') #없으면 None으로 저장
        upload_time = time.strftime('%Y %B %c')

        file_path = None
        if upload_file and upload_file.filename != '':
            orig_filename = upload_file.filename
            safe_filename = secure_filename(orig_filename)
            ext = os.path.splitext(safe_filename)[1] #확장자 추출
            final_filename = str(int(time.time())) + '_' + str(uuid.uuid4()) + ext
            file_path = os.path.join(UPLOAD_FOLDER, final_filename) #파일 경로 합치기
            upload_file.save(file_path) #서버 폴더에 upload_file 저장하기
            file_path = file_path.replace('\\', '/') #윈도우 경로 슬래시 통일

        # feed_table에 받은 데이터를 새로 저장, id는 AUTO_INCREMENT 사용해서 NULL 전달.
        cur.execute("INSERT INTO feed_table VALUES (NULL, %s, %s, %s, %s);",
                    (user_id, upload_comment, file_path, upload_time))
        conn.commit()
        return redirect(url_for('feed'))


'''
@app.route('/feedSearch')
def feedSearch():
    return render_template('feedSearch.html')

@app.route('/feedSearch/<int:friend_id>')
def searchFriend(friend_id):
    return render_template('feedSearch.html')

'''


if __name__ == '__main__':
    try:
        app.run()
    finally:
        conn.close()

