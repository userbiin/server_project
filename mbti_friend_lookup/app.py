from flask import Blueprint, Flask, render_template, request
import sqlite3

lkup_bp = Blueprint('lkup', __name__)
app = Flask(__name__)

def get_compatible_mbti(mbti):
    compatibility = {
        'ENTJ': ['ISFP', 'INFP', 'ESFP', 'ESTP', 'ISTP', 'INTP'],
        'ENTP': ['ISFJ', 'ISTJ', 'ENTP', 'ESTJ', 'ESFJ', 'INFJ'],
        'INTJ': ['ESFP', 'ESTP', 'ISFP', 'INFP', 'INFJ', 'ENFP'],
        'INTP': ['ESFJ', 'ENFJ', 'ISFJ', 'INFJ', 'ESTJ', 'ISTJ'],
        'ESTJ': ['INFP', 'ISFP', 'INTP', 'ENTP', 'ISTP', 'ESFP'],
        'ESFJ': ['INTP', 'ISTP', 'ENTP', 'ENFP', 'INFP', 'ISTJ'],
        'ISTJ': ['ENFP', 'ENTP', 'ISFP', 'ESTP', 'ESFP'],
        'ISFJ': ['ENTP', 'ENFP', 'INTP', 'ISTP', 'ESFP', 'ESTP'],
        'ENFJ': ['ISTP', 'INTP', 'ESTP', 'ESFP', 'ENFJ', 'INFP'],
        'ENFP': ['ISTJ', 'ISFJ', 'ESFJ', 'ESTJ', 'INFJ', 'INTJ'],
        'INFJ': ['ESTP', 'ESFP', 'ISTP', 'INTP', 'ENFP', 'ENTP'],
        'INFP': ['ESTJ', 'ENTJ', 'INTJ', 'ISTJ', 'ENFJ'],
        'ESTP': ['INFJ', 'INTJ', 'ENFJ', 'ENTJ', 'ISFJ', 'ISTP'],
        'ESFP': ['INTJ', 'INFJ', 'ENTJ', 'ENFJ', 'ESTJ', 'ISTJ'],
        'ISTP': ['ENFJ', 'ESFJ', 'INFJ', 'ISFJ', 'ENTJ', 'ESTJ'],
        'ISFP': ['ENTJ', 'ESTJ', 'INTJ', 'ISTJ', 'ENFJ'],
    }
    return compatibility.get(mbti.upper(), [])

@app.route('/', methods=['GET', 'POST'])
def index():
    compatible = []
    my_mbti = ''
    if request.method == 'POST':
        my_mbti = request.form['my_mbti']
        compatible = get_compatible_mbti(my_mbti)
    return render_template('index.html', compatible=compatible, my_mbti=my_mbti)

@app.route('/search')
def search():
    target_mbti = request.args.get('target_mbti')
    results = []
    if target_mbti:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT name, mbti FROM users WHERE mbti = ?", (target_mbti,))
        results = cur.fetchall()
        conn.close()
    return render_template('results.html', target_mbti=target_mbti, results=results)

if __name__ == '__main__':
    app.run(debug=True)
