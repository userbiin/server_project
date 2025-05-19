from flask import Blueprint, render_template, request, redirect, url_for, session
import os, pymysql

mbti_feature_bp = Blueprint('mbti_feature', __name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 폴더 없으면 자동생성 해줌.


db = pymysql.connect(host='localhost', user='flaskuser', password='1234', db='mbti_db', charset='utf8')
cursor = db.cursor()




#mbti 설명 파일 읽어오기
mbtiTxtFile = open('static/mbtiFeature/detail.txt','r', encoding='UTF8')
mbtiTxtText = mbtiTxtFile.read()
mbtiDetailList = [i.split(':') for i in mbtiTxtText.split('%')]
mbtiDetailDic = {}
for mbti in mbtiDetailList:
    mbtiDetailDic[mbti[0]] = mbti[1]


@mbti_feature_bp.route('/mbtiFeature', methods=['GET', 'POST'])
def mbti_feature():
    if 'login_id' not in session:
        return redirect(url_for('login.login'))

    CURRENT_USER_ID = session['login_id']  # 현재 로그인 사용자 ID

    if (request.method == 'GET'):
        mbti = request.args.get("type")
        if mbti:
            # 제목 및 상세 설명 담기
            detail = [mbti, mbtiDetailDic[mbti]]
            # 댓글 가져오기
            cursor.execute("SELECT * FROM mbti_comments WHERE target_mbti=%s", (mbti,))
            table = cursor.fetchall()

            return render_template('mbtiFeatureDetail.html', detail=detail, table=table, user_id=CURRENT_USER_ID)

        else:
            return render_template('mbtiFeatureBasic.html')
    elif (request.method == 'POST'):
        action = request.form.get("action")
        post_mbti = request.form.get("type")
        if action == "upload":
            comment = request.form.get("comment")
            cursor.execute(" INSERT INTO mbti_comments (target_mbti, user_id, comment) VALUES (%s, %s, %s);", (post_mbti, CURRENT_USER_ID, comment))
            db.commit()
            return redirect(url_for('mbti_feature.mbti_feature', type=post_mbti))
        elif action == "delete":
            delete_id = request.form['delete_id']
            cursor.execute("DELETE FROM mbti_comments WHERE id=%s", (delete_id,))
            db.commit()
            return redirect(url_for('mbti_feature.mbti_feature', type=post_mbti))


