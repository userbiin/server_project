from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_compatible_mbti(mbti):
    compatibility = {
        'ENTJ': ['ISFP', 'INFP', 'ESFP', 'ESTP', 'ISTP', 'INTP'],
        'ENTP': ['ISFJ', 'ISTJ', 'ENTP', 'ESTJ', 'ESFJ', 'INFJ'],
        'INTJ': ['ESFP', 'ESTP', 'ISFP', 'INFP', 'INFJ', 'ENFP'],
        'INTP': ['ESFJ', 'ENFJ', 'ISFJ', 'INFJ', 'ESTJ', 'ISTJ'],
        'ESTJ': ['INFP', 'ISFP', 'INTP', 'ENTP', 'ISTP', 'ESFP'],
      'ESFJ': ['INTP', 'ISTP', 'ENTP', 'ENFP', 'INFP', 'ISTJ'],
        'ISTJ': ['ENFP', 'ENTP', 'ISFP', 'ESTP', 'ESTP', 'ESFP'],
      'ISFJ': ['ENTP', 'ENFP', 'INTP', 'ISTP', 'ESFP', 'ESTP'],
      'ENFJ': ['ISTP', 'INTP', 'ESTP', 'ESFP', 'ENFJ', 'INFP'],
      'ENFP': ['ISTJ', 'ISFJ', 'ESFJ', 'ESTJ', 'INFJ', 'INTJ'],
      'INFJ': ['ESTP', 'ESFP', 'ISTP', 'INTP', 'ENFP', 'ENTP'],
      'INFP': ['ESTJ', 'ENTJ', 'INTJ', 'ISTJ', 'ENFJ', 'ENFJ'],
      'ESTP': ['INFJ', 'INTJ', 'ENFJ', 'ENTJ', 'ISFJ', 'ISTP'],
      'ESFP': ['INTJ', 'INFJ', 'ENTJ', 'ENFJ', 'ESTJ', 'ISTJ'],
      'ISTP': ['ENFJ', 'ESFJ', 'INFJ', 'ISFJ', 'ENTJ', 'ESTJ'],
      'ISFP': ['ENTJ', 'ESTJ', 'INTJ', 'ISTJ', 'ENFJ', 'ENFJ'],
        
    }
    return compatibility.get(mbti.upper(), [])

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    my_mbti = ''
    if request.method == 'POST':
        my_mbti = request.form['my_mbti']
        compatible = get_compatible_mbti(my_mbti)

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        query = "SELECT name, mbti FROM users WHERE mbti IN ({})".format(
            ','.join(['?'] * len(compatible))
        )
        cur.execute(query, compatible)
        results = cur.fetchall()
        conn.close()

    return render_template('index.html', results=results, my_mbti=my_mbti)

if __name__ == '__main__':
    app.run(debug=True)
