from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit, disconnect
import json
from datetime import datetime

app = Flask(__name__, static_folder='.')
app.config['SECRET_KEY'] = 'spidy-chat-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

messages = []
online_users = {}
CLEAR_PASSWORD = '872652'
ADMIN_PASSWORD = '8726520'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    online_users[sid] = {'name': 'Guest', 'connected_at': datetime.now().isoformat()}
    emit('all_messages', messages)
    emit('user_count', len(online_users), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in online_users:
        del online_users[sid]
    emit('user_count', len(online_users), broadcast=True)

@socketio.on('update_username')
def handle_update_username(data):
    sid = request.sid
    if sid in online_users:
        online_users[sid]['name'] = data.get('name', 'Guest')

@socketio.on('send_message')
def handle_message(data):
    message = {
        'name': data.get('name', 'Guest'),
        'text': data.get('text', ''),
        'ts': int(datetime.now().timestamp() * 1000),
        'id': len(messages),
        'seen_by': []
    }
    messages.append(message)
    emit('new_message', message, broadcast=True)

@socketio.on('mark_seen')
def handle_mark_seen(data):
    msg_id = data.get('msg_id')
    username = data.get('username')
    if 0 <= msg_id < len(messages):
        if username not in messages[msg_id]['seen_by']:
            messages[msg_id]['seen_by'].append(username)

@socketio.on('clear_messages')
def handle_clear(data):
    password = data.get('password', '')
    if password == CLEAR_PASSWORD:
        messages.clear()
        emit('messages_cleared', broadcast=True)
    else:
        emit('clear_failed', {'error': 'Invalid password'})

@socketio.on('get_messages')
def handle_get_messages():
    emit('all_messages', messages)

@socketio.on('admin_login')
def handle_admin_login(data):
    password = data.get('password', '')
    if password == ADMIN_PASSWORD:
        emit('admin_login_success')
    else:
        emit('admin_login_failed', {'error': 'Invalid admin password'})

@socketio.on('get_online_users')
def handle_get_online_users(data):
    password = data.get('password', '')
    if password == ADMIN_PASSWORD:
        users_list = [{'sid': sid, 'name': info['name'], 'connected_at': info['connected_at']} 
                     for sid, info in online_users.items()]
        emit('online_users_list', users_list)
    else:
        emit('admin_login_failed', {'error': 'Invalid admin password'})

@socketio.on('kick_user')
def handle_kick_user(data):
    password = data.get('password', '')
    target_sid = data.get('sid', '')
    if password == ADMIN_PASSWORD:
        if target_sid in online_users:
            socketio.server.disconnect(target_sid)
            emit('user_kicked', {'sid': target_sid}, broadcast=True)
    else:
        emit('admin_login_failed', {'error': 'Invalid admin password'})

@socketio.on('get_message_seen')
def handle_get_message_seen(data):
    password = data.get('password', '')
    msg_id = data.get('msg_id')
    if password == ADMIN_PASSWORD:
        if 0 <= msg_id < len(messages):
            emit('message_seen_info', {
                'msg_id': msg_id,
                'seen_by': messages[msg_id]['seen_by'],
                'message': messages[msg_id]['text']
            })
    else:
        emit('admin_login_failed', {'error': 'Invalid admin password'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
