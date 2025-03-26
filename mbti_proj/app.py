from flask import Flask

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html') 

@app.route('/user_register')
def user_register():
    return render_template('user_register.html') 

if __name__ == '__main__':
    app.run(debug = True)