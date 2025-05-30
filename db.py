import pymysql

db = pymysql.connect(
    host='127.0.0.1',
    user='flaskuser',
    password='1234',
    database='mbti_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
