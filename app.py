# from flask import Flask, render_template, request
# import sqlite3

# app = Flask(__name__)

# # MBTI 궁합 딕셔너리
# def get_compatible_mbti(mbti):
#     compatibility = {
#         'ENTJ': ['ISFP', 'INFP', 'ESFP', 'ESTP', 'ISTP', 'INTP'],
#         'ENTP': ['ISFJ', 'ISTJ', 'ENTP', 'ESTJ', 'ESFJ', 'INFJ'],
#         'INTJ': ['ESFP', 'ESTP', 'ISFP', 'INFP', 'INFJ', 'ENFP'],
#         'INTP': ['ESFJ', 'ENFJ', 'ISFJ', 'INFJ', 'ESTJ', 'ISTJ'],
#         'ESTJ': ['INFP', 'ISFP', 'INTP', 'ENTP', 'ISTP', 'ESFP'],
#         'ESFJ': ['INTP', 'ISTP', 'ENTP', 'ENFP', 'INFP', 'ISTJ'],
#         'ISTJ': ['ENFP', 'ENTP', 'ISFP', 'INFP', 'ESTP', 'ESFP'],
#         'ISFJ': ['ENTP', 'ENFP', 'INTP', 'ISTP', 'ESFP', 'ESTP'],
#         'ENFJ': ['ISTP', 'INTP', 'ESTP', 'ESFP', 'ENFJ', 'INFP'],
#         'ENFP': ['ISTJ', 'ISFJ', 'ESFJ', 'ESTJ', 'INFJ', 'INTJ'],
#         'INFJ': ['ESTP', 'ESFP', 'ISTP', 'INTP', 'ENFP', 'ENTP'],
#         'INFP': ['ESTJ', 'ENTJ', 'INTJ', 'ISTJ', 'ENFJ', 'ESFJ'],
#         'ESTP': ['INFJ', 'INTJ', 'ENFJ', 'ENTJ', 'ISFJ', 'ISTP'],
#         'ESFP': ['INTJ', 'INFJ', 'ENTJ', 'ENFJ', 'ESTJ', 'ISTJ'],
#         'ISTP': ['ENFJ', 'ESFJ', 'INFJ', 'ISFJ', 'ENTJ', 'ESTJ'],
#         'ISFP': ['ENTJ', 'ESTJ', 'INTJ', 'ISTJ', 'ENFJ', 'ESFJ'],
#     }
#     return compatibility.get(mbti.upper(), [])

# # 사용자 피드 보기 라우트
# @app.route('/user/<name>')
# def user_feed(name):
#     conn = sqlite3.connect('flaskuser.db')
#     cur = conn.cursor()
#     cur.execute("SELECT name, mbti, feed FROM users WHERE name = ?", (name,))
#     user = cur.fetchone()
#     conn.close()

#     if user:
#         return render_template('user_feed.html', user=user)
#     else:
#         return "사용자를 찾을 수 없습니다.", 404

# # 메인 페이지 (MBTI 입력)
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     my_mbti = ''
#     compatible = []
#     if request.method == 'POST':
#         my_mbti = request.form['my_mbti']
#         compatible = get_compatible_mbti(my_mbti)
#     return render_template('index.html', my_mbti=my_mbti, compatible=compatible)

# # 결과 페이지 (해당 MBTI 사용자 조회)
# @app.route('/results')
# def results():
#     mbti = request.args.get('mbti')
#     conn = sqlite3.connect('flaskuser.db')
#     cur = conn.cursor()
#     cur.execute("SELECT name, mbti FROM users WHERE mbti = ?", (mbti,))
#     results = cur.fetchall()
#     conn.close()
#     return render_template('results.html', mbti=mbti, results=results)

# # 서버 실행
# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# MySQL 연결 함수
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1234',  # 너가 설정한 비밀번호
        database='mbti_app',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.Cursor
    )

# MBTI 궁합 딕셔너리
def get_compatible_mbti(mbti):
    compatibility = {
        'ENTJ': ['ISFP', 'INFP', 'ESFP', 'ESTP', 'ISTP', 'INTP'],
        'ENTP': ['ISFJ', 'ISTJ', 'ENTP', 'ESTJ', 'ESFJ', 'INFJ'],
        'INTJ': ['ESFP', 'ESTP', 'ISFP', 'INFP', 'INFJ', 'ENFP'],
        'INTP': ['ESFJ', 'ENFJ', 'ISFJ', 'INFJ', 'ESTJ', 'ISTJ'],
        'ESTJ': ['INFP', 'ISFP', 'INTP', 'ENTP', 'ISTP', 'ESFP'],
        'ESFJ': ['INTP', 'ISTP', 'ENTP', 'ENFP', 'INFP', 'ISTJ'],
        'ISTJ': ['ENFP', 'ENTP', 'ISFP', 'INFP', 'ESTP', 'ESFP'],
        'ISFJ': ['ENTP', 'ENFP', 'INTP', 'ISTP', 'ESFP', 'ESTP'],
        'ENFJ': ['ISTP', 'INTP', 'ESTP', 'ESFP', 'ENFJ', 'INFP'],
        'ENFP': ['ISTJ', 'ISFJ', 'ESFJ', 'ESTJ', 'INFJ', 'INTJ'],
        'INFJ': ['ESTP', 'ESFP', 'ISTP', 'INTP', 'ENFP', 'ENTP'],
        'INFP': ['ESTJ', 'ENTJ', 'INTJ', 'ISTJ', 'ENFJ', 'ESFJ'],
        'ESTP': ['INFJ', 'INTJ', 'ENFJ', 'ENTJ', 'ISFJ', 'ISTP'],
        'ESFP': ['INTJ', 'INFJ', 'ENTJ', 'ENFJ', 'ESTJ', 'ISTJ'],
        'ISTP': ['ENFJ', 'ESFJ', 'INFJ', 'ISFJ', 'ENTJ', 'ESTJ'],
        'ISFP': ['ENTJ', 'ESTJ', 'INTJ', 'ISTJ', 'ENFJ', 'ESFJ'],
    }
    return compatibility.get(mbti.upper(), [])

# 메인 페이지
@app.route('/', methods=['GET', 'POST'])
def index():
    my_mbti = ''
    compatible = []
    if request.method == 'POST':
        my_mbti = request.form['my_mbti']
        compatible = get_compatible_mbti(my_mbti)
    return render_template('index.html', my_mbti=my_mbti, compatible=compatible)

# 결과 페이지
@app.route('/results')
def results():
    mbti = request.args.get('mbti')
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT name, mbti FROM users WHERE mbti = %s", (mbti,))
        results = cur.fetchall()
    conn.close()
    return render_template('results.html', mbti=mbti, results=results)

# 사용자 상세 페이지 (소개 포함)
@app.route('/user/<name>')
def user_feed(name):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT name, mbti, introduction FROM users WHERE name = %s", (name,))
        user = cur.fetchone()
    conn.close()
    if user:
        return render_template('user_feed.html', user=user)
    else:
        return "사용자를 찾을 수 없습니다.", 404

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True)
