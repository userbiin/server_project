from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector

friend_bp = Blueprint('friend', __name__)
db = mysql.connector.connect(
    host="localhost", 
    user="flaskuser",  # mysql 새사용자 생성->flaskuser
    password="1234", 
    database="mbti_db")

cursor = db.cursor(dictionary=True) # 데이터 dict 형태로 전달
CURRENT_USER_ID = 1

@friend_bp.route('/friends')
def show_friends_page():
    # 친구 요청
    cursor.execute("""
        SELECT f.id, u.name, u.mbti
        FROM friends f
        JOIN users u ON f.user_id = u.id
        WHERE f.friend_id = %s AND f.status = 'pending'
    """, (CURRENT_USER_ID,))
    pending_requests = cursor.fetchall()

    # 친구 목록 조회
    cursor.execute("""
        SELECT u.id, u.name, u.mbti
        FROM friends f
        JOIN users u ON u.id = 
            CASE 
                WHEN f.user_id = %s THEN f.friend_id
                ELSE f.user_id
            END
        WHERE (f.user_id = %s OR f.friend_id = %s)
          AND f.status = 'accepted'
    """, (CURRENT_USER_ID, CURRENT_USER_ID, CURRENT_USER_ID))
    friends = cursor.fetchall()

    return render_template('friendpage.html',
                           pending_requests=pending_requests,
                           friends=friends,
                           search_result=None,
                           searched=False)

# 친구 요청 수락     
@friend_bp.route('/accept_friend/<int:request_id>', methods=['POST'])
def accept_friend(request_id):
    cursor.excute("""
                  UPDATE freinds
                  SET status = 'accept'
                  WHERE id =%s
                  """, (request_id))
    db.commit()
    return redirect(url_for('friend.show_friends_page'))


# 친구 삭제
@friend_bp.route('/delete_friend/<int:friend_id>', methods=['POST'])
def delete_friend(friend_id):
    # user_id <-> friend_id 양방향 고려
    cursor.execute("""
        DELETE FROM friends
        WHERE 
            (user_id = %s AND friend_id = %s)
            OR
            (user_id = %s AND friend_id = %s)
    """, (CURRENT_USER_ID, friend_id, friend_id, CURRENT_USER_ID))
    db.commit()
    return redirect(url_for('friend.show_friends_page'))
