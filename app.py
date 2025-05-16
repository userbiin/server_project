# 메인 홈페이지 
from flask import Flask, render_template, session
import sys
import os

# 다른 리포지토리 경로 불러오기 모듈 추가 
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from feature_friend.friend import friend_bp
from mbti_friend_lookup.app import lkup_bp
from mbti_proj.app import app
from feature_friend.friend import friend_bp # feature/feed app.py 이름 수정 필요

app = Flask(__name__)
app.register_blueprint(friend_bp, url_prefix='/friend')
app.register_blueprint(lkup_bp, url_prefix='/lookup')
app.register_blueprint(app, url_prefix='/login')



# 테스트용
app.secret_key = 'any-random-string'  # 세션 사용을 위한 키 임시부여

@app.before_request
def simulate_login():
    session['user_id'] = 4  # 'user2'의 id라고 가정

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)