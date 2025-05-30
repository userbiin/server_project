from flask import Blueprint, render_template, request, redirect, url_for, session
import pymysql

friend_bp = Blueprint('friend', __name__)

from db import db


@friend_bp.route('/friends')
def show_friends_page():
    CURRENT_USER_ID = session.get('user_id')
    if not CURRENT_USER_ID:
        return redirect(url_for('login.login'))

    with db.cursor() as cursor:
        cursor.execute("""
            SELECT f.id, u.name, u.mbti
            FROM friends f
            JOIN users u ON f.user_id = u.id
            WHERE f.friend_id = %s AND f.status = 'pending'
        """, (CURRENT_USER_ID,))
        pending_requests = cursor.fetchall()

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


@friend_bp.route('/accept_friend/<int:request_id>', methods=['POST'])
def accept_friend(request_id):
    CURRENT_USER_ID = session.get('user_id')
    if not CURRENT_USER_ID:
        return redirect(url_for('login.login'))

    with db.cursor() as cursor:
        cursor.execute("""
            UPDATE friends
            SET status = 'accepted'
            WHERE id = %s
        """, (request_id,))

        cursor.execute("SELECT user_id, friend_id FROM friends WHERE id = %s", (request_id,))
        result = cursor.fetchone()

        if result:
            user_id = result['user_id']
            friend_id = result['friend_id']

            cursor.execute("""
                SELECT COUNT(*) as cnt FROM friends
                WHERE user_id = %s AND friend_id = %s
            """, (friend_id, user_id))
            count_result = cursor.fetchone()

            if count_result['cnt'] == 0:
                cursor.execute("""
                    INSERT INTO friends (user_id, friend_id, status)
                    VALUES (%s, %s, 'accepted')
                """, (friend_id, user_id))

    db.commit()
    return redirect(url_for('friend.show_friends_page'))


@friend_bp.route('/delete_friend/<int:friend_id>', methods=['POST'])
def delete_friend(friend_id):
    CURRENT_USER_ID = session.get('user_id')
    if not CURRENT_USER_ID:
        return redirect(url_for('login.login'))

    with db.cursor() as cursor:
        cursor.execute("""
            DELETE FROM friends
            WHERE (user_id = %s AND friend_id = %s)
               OR (user_id = %s AND friend_id = %s)
        """, (CURRENT_USER_ID, friend_id, friend_id, CURRENT_USER_ID))
    db.commit()
    return redirect(url_for('login.mypage'))


@friend_bp.route('/search_user', methods=['POST'])
def search_user():
    CURRENT_USER_ID = session.get('user_id')
    if not CURRENT_USER_ID:
        return redirect(url_for('login.login'))

    username = request.form['username']

    with db.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM users 
            WHERE name = %s AND id != %s
        """, (username, CURRENT_USER_ID))
        results = cursor.fetchall()

        cursor.execute("""
            SELECT f.id, u.name, u.mbti
            FROM friends f
            JOIN users u ON f.user_id = u.id
            WHERE f.friend_id = %s AND f.status = 'pending'
        """, (CURRENT_USER_ID,))
        pending_requests = cursor.fetchall()

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


@friend_bp.route('/request_friend', methods=['POST'])
def request_friend():
    CURRENT_USER_ID = session.get('user_id')
    if not CURRENT_USER_ID:
        return redirect(url_for('login.login'))

    friend_id = request.form['friend_id']

    with db.cursor() as cursor:
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
