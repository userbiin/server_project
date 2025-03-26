from flask import Blueprint, render_template
import mysql.connector

friend_bp = Blueprint('friend', __name__)
db = mysql.connector.connect(
    host="localhost", 
    user="flaskuser", 
    password="1234", 
    database="mbti_db")

cursor = db.cursor(dictionary=True)
CURRENT_USER_ID = 1

@friend_bp.route('/friends')
def show_friends_page():
    # ✅ 1. 받은 친구 요청 (나에게 온 요청 중 아직 수락하지 않은 것)
    cursor.execute("""
        SELECT f.id, u.name, u.mbti
        FROM friends f
        JOIN users u ON f.user_id = u.id
        WHERE f.friend_id = %s AND f.status = 'pending'
    """, (CURRENT_USER_ID,))
    pending_requests = cursor.fetchall()

    # ✅ 2. 친구 목록 (내가 수락한 친구 관계)
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

    return render_template('freindpage.html',
                           pending_requests=pending_requests,
                           friends=friends,
                           search_result=None,
                           searched=False)
