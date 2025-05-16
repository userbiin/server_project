import sqlite3

conn = sqlite3.connect('flaskuser.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    mbti TEXT NOT NULL,
    feed TEXT DEFAULT ''  -- 추가: 사용자 피드 내용
)
''')

dummy_data = [
    ('Alice', 'INFJ', '오늘은 날씨가 참 좋네요. 친구들과 카페에 갔어요!'),
    ('Bob', 'INTJ', '책을 읽으며 조용한 하루를 보냈습니다.'),
    ('Carol', 'ENFP', '새로운 프로젝트를 시작했어요! 너무 신나요.'),
    ('Dave', 'ISFJ', '가족과 함께 시간을 보내며 힐링했어요.'),
    ('Eve', 'ESTP', '액티비티가 최고! 클라이밍을 즐겼어요.'),
    ('Frank', 'ENFP', '밝고 즐거운 하루였어요.')
]

conn.executemany('INSERT INTO users (name, mbti, feed) VALUES (?, ?, ?)', dummy_data)

conn.commit()
conn.close()
print("DB 생성 완료!")
