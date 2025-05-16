from flask import Flask
from feed_routes import feed_bp
from mbti_feature_routes import mbti_feature_bp

app = Flask(__name__)
app.register_blueprint(feed_bp)
app.register_blueprint(mbti_feature_bp)

if __name__ == '__main__':
    app.run()
