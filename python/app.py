import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from RAGTest import get_response
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)
CORS(app)
app.logger.setLevel(logging.DEBUG)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50))
    message = db.Column(db.String(500))
    sender = db.Column(db.String(50))

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/new_session', methods=['POST'])
def new_session():
    session_id = str(uuid.uuid4())
    return jsonify({'session_id': session_id})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    session_id = data['session_id']
    message = data['message']

    # 保存用户消息
    user_chat = ChatHistory(session_id=session_id, message=message, sender='User')
    db.session.add(user_chat)
    db.session.commit()

    # 获取当前会话的历史记录
    history = ChatHistory.query.filter_by(session_id=session_id).all()
    chat_history = [{'message': chat.message, 'sender': chat.sender} for chat in history]

    # 提取历史记录中的消息部分
    history_messages = [chat['message'] for chat in chat_history]
    app.logger.debug(history_messages)
    # 使用自定义函数生成AI回复
    ai_response = get_response(message, history_messages)

    # 保存AI回复
    ai_chat = ChatHistory(session_id=session_id, message=ai_response, sender='AI')
    db.session.add(ai_chat)
    db.session.commit()

    return jsonify({'response': ai_response})

@app.route('/get_history/<session_id>', methods=['GET'])
def get_history(session_id):
    chats = ChatHistory.query.filter_by(session_id=session_id).all()
    history = [{'message': chat.message, 'sender': chat.sender} for chat in chats]
    return jsonify({'history': history})

@app.route('/get_sessions', methods=['GET'])
def get_sessions():
    sessions = db.session.query(ChatHistory.session_id).distinct().all()
    return jsonify({'sessions': [s[0] for s in sessions]})

@app.route('/delete_session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    ChatHistory.query.filter_by(session_id=session_id).delete()
    db.session.commit()
    return jsonify({'message': f'Session {session_id} deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
