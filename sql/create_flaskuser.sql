CREATE USER IF NOT EXISTS 'flaskuser'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON mbti_db.* TO 'flaskuser'@'localhost';
FLUSH PRIVILEGES;
# sql사용자 비밀번호 1234