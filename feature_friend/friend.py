from flask import Blueprint, render_template, request, redirect, url_for, session
import mysql.connector

friend_bp = Blueprint('friend', __name__)
db = mysql.connector.connect(
    host="localhost",
    user="flaskuser",
    password="1234",
    database="mbti_db"
)
cursor = db.cursor(dictionary=True)

@friend_bp.route('/friends')
def show_friends_page():
    CURRENT_USER_ID = session.get('user_id')
    if not CURRENT_USER_ID:
        return redirect(url_for('login.login'))

    # 받은 친구 요청 (상대방이 보낸 pending 상태)
    cursor.execute("""
        SELECT f.id, u.name, u.mbti
        FROM friends f
        JOIN users u ON f.user_id = u.id
        WHERE f.friend_id = %s AND f.status = 'pending'
    """, (CURRENT_USER_ID,))
    pending_requests = cursor.fetchall()

    # 친구 목록 (accepted 상태의 친구만 표시)
    cursor.execute("""
        SELECT u.id, u.name, u.mbti
        FROM friends f
        JOIN users u ON u.id = f.friend_id
        WHERE f.user_id = %s AND f.status = 'accepted'
    """, (CURRENT_USER_ID,))
    friends = cursor.fetchall()

    return render_template('friendpage.html',
                           pending_requests=pending_requests,
                           friends=friends,
                           search_result=None,
                           searched=False)

# 친구 요청 수락 및 쌍방 INSERT
@friend_bp.route('/accept_friend/<int:request_id>', methods=['POST'])
def accept_friend(request_id):
    CURRENT_USER_ID = session.get('user_id')
    if not CURRENT_USER_ID:
        return redirect(url_for('login.login'))

    # 요청 수락 (상태 변경)
    cursor.execute("""
        UPDATE friends
        SET status = 'accepted'
        WHERE id = %s
    """, (request_id,))

    # 요청자와 수신자 정보 가져오기
    cursor.execute("SELECT user_id, friend_id FROM friends WHERE id = %s", (request_id,))
    result = cursor.fetchone()

    if result:
        user_id = result['user_id']
        friend_id = result['friend_id']

        # 반대 방향 존재 여부 확인
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM friends
            WHERE user_id = %s AND friend_id = %s
        """, (friend_id, user_id))
        count_result = cursor.fetchone()

        # 존재하지 않으면 쌍방 INSERT
        if count_result['cnt'] == 0:
            cursor.execute("""
                INSERT INTO friends (user_id, friend_id, status)
                VALUES (%s, %s, 'accepted')
            """, (friend_id, user_id))

    db.commit()
    return redirect(url_for('friend.show_friends_page'))

# 친구 삭제 (양방향 모두 삭제)
@friend_bp.route('/delete_friend/<int:friend_id>', methods=['POST'])
def delete_friend(friend_id):
    CURRENT_USER_ID = session.get('user_id')
    if not CURRENT_USER_ID:
        return redirect(url_for('login.login')) 

    cursor.execute("""
        DELETE FROM friends
        WHERE (user_id = %s AND friend_id = %s)
           OR (user_id = %s AND friend_id = %s)
    """, (CURRENT_USER_ID, friend_id, friend_id, CURRENT_USER_ID))
    db.commit()
    return redirect(url_for('friend.show_friends_page'))

# 사용자 검색
@friend_bp.route('/search_user', methods=['POST'])
def search_user():
    CURRENT_USER_ID = session.get('user_id')
    if not CURRENT_USER_ID:
        return redirect(url_for('login.login'))

    username = request.form['username']

    # 자기 자신은 제외한 이름 검색
    cursor.execute("""
        SELECT * FROM users 
        WHERE name = %s AND id != %s
    """, (username, CURRENT_USER_ID))
    results = cursor.fetchall()

    # 받은 요청
    cursor.execute("""
        SELECT f.id, u.name, u.mbti
        FROM friends f
        JOIN users u ON f.user_id = u.id
        WHERE f.friend_id = %s AND f.status = 'pending'
    """, (CURRENT_USER_ID,))
    pending_requests = cursor.fetchall()

    # 친구 목록
    cursor.execute("""
        SELECT u.id, u.name, u.mbti
        FROM friends f
        JOIN users u ON u.id = f.friend_id
        WHERE f.user_id = %s AND f.status = 'accepted'
    """, (CURRENT_USER_ID,))
    friends = cursor.fetchall()

    return render_template('friendpage.html',
                           pending_requests=pending_requests,
                           friends=friends,
                           search_result=results,
                           searched=True)



# 친구 요청 보내기
@friend_bp.route('/request_friend', methods=['POST'])
def request_friend():
    CURRENT_USER_ID = session.get('user_id')
    if not CURRENT_USER_ID:
        return redirect(url_for('login.login'))

    friend_id = request.form['friend_id']

    # 중복 요청 방지
    cursor.execute("""
        SELECT COUNT(*) as cnt FROM friends
        WHERE user_id = %s AND friend_id = %s
    """, (CURRENT_USER_ID, friend_id))
    if cursor.fetchone()['cnt'] == 0:
        cursor.execute("""
            INSERT INTO friends (user_id, friend_id, status)
            VALUES (%s, %s, 'pending')
        """, (CURRENT_USER_ID, friend_id))
        db.commit()

    return redirect(url_for('friend.show_friends_page'))
