from flask import Flask, render_template, session
import sys
import os

# 다른 리포지토리 경로 불러오기 모듈 추가 
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from feature_friend.friend import friend_bp

app = Flask(__name__)
app.register_blueprint(friend_bp)
# 테스트용
app.secret_key = 'any-random-string'  # 세션 사용을 위한 키 임시부여

@app.before_request
def simulate_login():
    session['user_id'] = 4  # 'user2'의 id라고 가정

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


