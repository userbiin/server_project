from flask import Flask, render_template, session
import sys, os
from feature_user.login import user_app
from feature_feed.feed_routes import feed_bp
from feature_feed.mbti_feature_routes import mbti_feature_bp
from feature_find.find_routes import find_bp
from feature_friend.friend import friend_bp

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)
app.register_blueprint(friend_bp)
app.register_blueprint(user_app, url_prefix='/login')
app.register_blueprint(find_bp)
app.register_blueprint(mbti_feature_bp)
app.register_blueprint(feed_bp)

# 테스트용
app.secret_key = 'any-random-string'  # 세션 사용을 위한 키 임시부여
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)