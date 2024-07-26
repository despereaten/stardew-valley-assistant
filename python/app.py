import logging
from flask import Flask, request, jsonify,Response
import requests

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from RAGTest import get_response,summarize_dialog,RAG_stream
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)
CORS(app)
app.logger.setLevel(logging.DEBUG)


from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app.config['JWT_SECRET_KEY'] = 'gnxSnJ55YhWWQvvOdzPlthCRUfRwEqCiIE_Y39ntuJM'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), unique=True, nullable=False)
    summary = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))


class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    sender = db.Column(db.String(50), nullable=False)
    session_id = db.Column(db.String(50), db.ForeignKey('session.session_id'), nullable=False)
    session = db.relationship('Session', backref=db.backref('chats', lazy=True))


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


# 创建数据库表
with app.app_context():
    # db.drop_all()
    db.create_all()


@app.route('/new_session', methods=['POST'])
@jwt_required()
def new_session():
    user_id = get_jwt_identity()
    session_id = str(uuid.uuid4())
    summary = "新会话"
    new_session = Session(session_id=session_id, summary=summary, user_id=user_id)
    db.session.add(new_session)
    db.session.commit()

    initial_message = "你好，有什么能帮到你"
    new_chat_history = ChatHistory(message=initial_message, sender="", session_id=session_id)
    db.session.add(new_chat_history)
    db.session.commit()

    return jsonify({'session_id': session_id, 'summary': summary})


@app.route('/send_message', methods=['POST'])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = request.json
    session_id = data['session_id']
    message = data['message']

    # 获取当前会话的chathistory条目
    session_entry = Session.query.filter_by(session_id=session_id, user_id=user_id).first()
    # if not session_entry:
    #     return jsonify({'message': 'Session not found'}), 404

    # 更新会话概括内容(如果当前会话的概括内容是"新对话")
    if session_entry.summary == "新会话":
        session_entry.summary = summarize_dialog(message)
        db.session.commit()

    # 保存用户信息
    user_chat = ChatHistory(session_id=session_id, message=message, sender='User')
    db.session.add(user_chat)
    db.session.commit()

    # 获取当前会话的历史记录
    history = ChatHistory.query.filter_by(session_id=session_id).all()
    chat_history = [{'message': chat.message, 'sender': chat.sender} for chat in history]

    # 提取历史记录中的消息部分
    history_messages = [chat['message'] for chat in chat_history if chat['message']]
    app.logger.debug(history_messages)

    # 生成流式回复
    return Response(RAG_stream(message,history_messages),mimetype = 'text/plain')

@app.route('/save_answer', methods=['POST'])
def save_answer():
    data = request.json
    session_id = data['session_id']
    answer = data['answer']
    try:
        ai_chat = ChatHistory(session_id=session_id, message=answer, sender='AI')
        db.session.add(ai_chat)
        db.session.commit()
        return jsonify({'status': 'success'}),200
    except Exception as e:
        # 如果出现异常，返回错误响应
        return jsonify({'status': 'error', 'message':str(e)}),500


@app.route('/update_summary/<session_id>', methods=['GET'])
def update_summary(session_id):
    session_entry = Session.query.filter_by(session_id=session_id).first()
    summary = session_entry.summary
    return jsonify({'session_id':session_id,'summary': summary})


@app.route('/get_history/<session_id>', methods=['GET'])
@jwt_required()
def get_history(session_id):
    user_id = get_jwt_identity()
    session_entry = Session.query.filter_by(session_id=session_id, user_id=user_id).first()
    if not session_entry:
        return jsonify({'message': 'Session not found'}), 404

    chats = ChatHistory.query.filter_by(session_id=session_id).all()
    history = [{'message': chat.message, 'sender': chat.sender} for chat in chats]
    return jsonify({'history': history})


@app.route('/get_sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    user_id = get_jwt_identity()
    sessions = Session.query.filter_by(user_id=user_id).all()
    return jsonify({'sessions': [{'session_id': s.session_id, 'summary': s.summary} for s in sessions]})


@app.route('/delete_session/<session_id>', methods=['DELETE'])
@jwt_required()
def delete_session(session_id):
    user_id = get_jwt_identity()
    session_entry = Session.query.filter_by(session_id=session_id, user_id=user_id).first()
    if not session_entry:
        return jsonify({'message': 'Session not found'}), 404

    ChatHistory.query.filter_by(session_id=session_id).delete()
    db.session.delete(session_entry)
    db.session.commit()
    return jsonify({'message': f'Session {session_id} deleted'}), 200

@app.route('/stream', methods=['POST'])
def stream_output():
    data = request.get_json()
    message = data.get('message')
    if data:
        return Response(RAG_stream(message,[]), mimetype='text/plain')
    return "没有内容"


if __name__ == '__main__':
    app.run(debug=True)

