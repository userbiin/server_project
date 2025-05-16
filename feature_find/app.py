from flask import Flask, render_template, request
import pymysql

find = Flask(__name__)  

# MySQL 연결 함수
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        database='mbti_app',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.Cursor
    )

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

@find.route('/', methods=['GET', 'POST'])
def index():
    my_mbti = ''
    compatible = []
    if request.method == 'POST':
        my_mbti = request.form['my_mbti']
        compatible = get_compatible_mbti(my_mbti)
    return render_template('index.html', my_mbti=my_mbti, compatible=compatible)

@find.route('/results')
def results():
    mbti = request.args.get('mbti')
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT name, mbti FROM users WHERE mbti = %s", (mbti,))
        results = cur.fetchall()
    conn.close()
    return render_template('results.html', mbti=mbti, results=results)

@find.route('/user/<name>')
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

if __name__ == '__main__':
    find.run(debug=True) 
