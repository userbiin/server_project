from flask import Flask, render_template 
import sys
import os

# 다른 리포지토리 경로 불러오기 모듈 추가 
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from feature_friend.friend import friend_bp

app = Flask(__name__)
app.register_blueprint(friend_bp)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


