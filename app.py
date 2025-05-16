from flask import Flask, render_template, session
import sys, os
from feature_feed.feed_routes import feed_bp
from feature_feed.mbti_feature_routes import mbti_feature_bp

app = Flask(__name__)
app.register_blueprint(feed_bp)
app.register_blueprint(mbti_feature_bp)


# 다른 리포지토리 경로 불러오기 모듈 추가 
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from feature_friend.friend import friend_bp
#from feature_user.login import user_app
#from feature_find.app import find
from feature_feed.mbti_feature_routes import mbti_feature_bp
from feature_feed.feed_routes import feed_bp

app = Flask(__name__)
app.register_blueprint(friend_bp)
#app.register_blueprint(user_app)
#app.register_blueprint(find)
app.register_blueprint(mbti_feature_bp)
app.register_blueprint(feed_bp)

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