import logging
from flask import Flask, request, jsonify, Response
import requests
import importlib
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from RAGTest import get_response, summarize_dialog, RAG_stream
from get_links import get_link
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
# 初始化实例以便进行数据库操作
db = SQLAlchemy(app)
CORS(app)
app.logger.setLevel(logging.DEBUG)

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app.config['JWT_SECRET_KEY'] = 'gnxSnJ55YhWWQvvOdzPlthCRUfRwEqCiIE_Y39ntuJM'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


# 会话模型
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), unique=True, nullable=False)
    summary = db.Column(db.String(100))  # , nullable=False
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.String(50), default="AI", nullable=False)  # 新增的列，默认值为 "AI"
    # 通过user_id字段与User模型建立外键关系。
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))


# 聊天历史模型:message为内容，sender为发送者
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    sender = db.Column(db.String(50), nullable=False)
    session_id = db.Column(db.String(50), db.ForeignKey('session.session_id'), nullable=False)
    # 通过session_id字段与Session模型建立外键关系。
    session = db.relationship('Session', backref=db.backref('chats', lazy=True))


# zy:推荐链接
class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    # title = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('recommendations', lazy=True))


# 用户注册
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


# 用户登录
@app.route('/login', methods=['POST'])
def login():
    data = request.json  # 从请求中提取JSON数据
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


# 创建数据库表
with app.app_context():
    #db.drop_all()
    db.create_all()


# 生成新对话
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


# 客户端发送消息
@app.route('/send_message', methods=['POST'])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = request.json
    session_id = data['session_id']
    message = data['message']  # 获取用户发送的消息

    # 获取当前会话的chathistory条目
    session_entry = Session.query.filter_by(session_id=session_id, user_id=user_id).first()
    # if not session_entry:
    #     return jsonify({'message': 'Session not found'}), 404

    # 更新会话概括内容(如果当前会话的概括内容是"新对话")
    if session_entry.summary == "新会话":
        session_entry.summary = summarize_dialog(message)
        db.session.commit()

    # 保存用户发送的消息到聊天历史记录
    user_chat = ChatHistory(session_id=session_id, message=message, sender='User')
    db.session.add(user_chat)
    db.session.commit()

    # 获取当前会话的所有历史记录
    history = ChatHistory.query.filter_by(session_id=session_id).all()
    chat_history = [{'message': chat.message, 'sender': chat.sender} for chat in history]

    # 提取历史记录中的消息部分
    history_messages = [chat['message'] for chat in chat_history if chat['message']]
    app.logger.debug(history_messages)

    # 生成流式回复
    return Response(RAG_stream(message, history_messages), mimetype='text/plain')


# 保存AI回复
@app.route('/save_answer', methods=['POST'])
def save_answer():
    data = request.json
    session_id = data['session_id']
    answer = data['answer']  # 从前端请求获取AI的回复
    try:
        ai_chat = ChatHistory(session_id=session_id, message=answer, sender='AI')
        db.session.add(ai_chat)
        db.session.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        # 如果出现异常，返回错误响应
        return jsonify({'status': 'error', 'message': str(e)}), 500


# 更新会话概要
@app.route('/update_summary/<session_id>', methods=['GET'])
def update_summary(session_id):
    session_entry = Session.query.filter_by(session_id=session_id).first()
    summary = session_entry.summary
    return jsonify({'session_id': session_id, 'summary': summary})


# 获取会话历史记录
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
    # 过滤 character_id 为 “AI” 的会话
    sessions = Session.query.filter_by(user_id=user_id, character_id="AI").all()
    return jsonify({'sessions': [{'session_id': s.session_id, 'summary': s.summary} for s in sessions]})


# 删除会话
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


# 流式返回生成的内容
@app.route('/stream', methods=['POST'])
def stream_output():
    data = request.get_json()
    message = data.get('message')
    if data:
        return Response(RAG_stream(message, []), mimetype='text/plain')
    return "没有内容"


# zy：
import random


@app.route('/generate_links', methods=['POST'])
@jwt_required()
def generate_link():
    user_id = get_jwt_identity()
    keytext = get_messages_by_session_and_sender(user_id)
    links = get_link(keytext)

    # 如果链接数量小于10,就全部返回
    if len(links) < 10:
        links = links
    else:
        # 从所有链接中随机选择10个
        links = random.sample(links, 10)

    # 删除旧的链接
    Recommendation.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    # 插入新的链接
    for link in links:
        new_recommendation = Recommendation(link=link, user_id=user_id)
        db.session.add(new_recommendation)
    db.session.commit()

    return jsonify({'links': links})



# chat相关
@app.route('/new_chat_session', methods=['POST'])
@jwt_required()
def new_chat_session():
    user_id = get_jwt_identity()
    data = request.json  # 获取请求中的JSON数据
    character_id = data['post_character_id']  # 获取character_id
    session_id = str(uuid.uuid4())
    summary = "人物对话"
    new_session = Session(session_id=session_id, summary=summary, user_id=user_id, character_id=character_id)
    db.session.add(new_session)
    db.session.commit()

    initial_message = "嗨？"
    new_chat_history = ChatHistory(message=initial_message, sender="", session_id=session_id)
    db.session.add(new_chat_history)
    db.session.commit()

    return jsonify({'session_id': session_id})


# zy
@app.route('/get_links', methods=['GET'])
@jwt_required()
def get_links():
    user_id = get_jwt_identity()
    recommendations = Recommendation.query.filter_by(user_id=user_id).all()
    # 提取链接列表
    links = [rec.link for rec in recommendations]
    return jsonify({'links': links})


# 获取用户最新的历史记录
def get_messages_by_session_and_sender(user_id):
    sessions = Session.query.filter_by(user_id=user_id).all()
    message_list = ['星露谷']

    # 如果获取到的记录超过5条，那么只根据用户最近查询的获取关键词
    if len(sessions) > 5:
        sessions = sessions[-5:]
    for session in sessions:
        messages = ChatHistory.query.filter_by(session_id=session.session_id, sender='User').all()
        if messages:
            message_list.extend([chat.message for chat in messages])
    print("最新词汇列表：", messages)
    # 返回消息列表
    return message_list


# 客户端发送消息
@app.route('/send_chat_message', methods=['POST'])
@jwt_required()
def send_chat_message():
    user_id = get_jwt_identity()
    data = request.json
    session_id = data['session_id']
    message = data['message']  # 获取用户发送的消息

    # 获取当前会话的chathistory条目
    session_entry = Session.query.filter_by(session_id=session_id, user_id=user_id).first()
    character_id = session_entry.character_id

    # 保存用户发送的消息到聊天历史记录
    user_chat = ChatHistory(session_id=session_id, message=message, sender='User')
    db.session.add(user_chat)
    db.session.commit()

    # 获取当前会话的所有历史记录
    history = ChatHistory.query.filter_by(session_id=session_id).all()
    chat_history = [{'message': chat.message, 'sender': chat.sender} for chat in history]

    # 提取历史记录中的消息部分
    history_messages = [chat['message'] for chat in chat_history if chat['message']]
    app.logger.debug(history_messages)

    # 生成流式回复
    return Response(chat_stream(message, history_messages, character_id, ), mimetype='text/plain')


def chat_stream(input, history, character_id):
    #动态导入，根据名字导入对应链条
    module_name = f"character_chains.{character_id}_role_chat"
    character_module = importlib.import_module(module_name)
    # 获取模块中的 llmchain 对象
    llmchain = character_module.chain

    for chunk in llmchain.stream({"question": input, "chat_history": history}):
        delta_content = chunk
        #delta_content = chunk.get("output")
        if delta_content:
            yield f"{delta_content}".encode('utf-8')
        else:
            yield "\n".encode('utf-8')


# zmj
from Role_Match import answers, roles, questions, zhipuai_chat_model


def generate_role_match_stream():
    with app.app_context():
        app.logger.debug(len(answers))
        if len(answers) < len(questions):
            next_question = questions[len(answers)]
            yield f'{next_question}'.encode('utf-8')
        else:
            combined_answers = " ".join(answers)
            prompt = f"根据以下回答，判断用户最适合的角色：\n\n回答：{combined_answers}\n\n角色定义：{roles}\n\n请给出用户最适合的角色并解释理由。"
            for chunk in zhipuai_chat_model.stream(input=prompt):
                delta_content = chunk.content
                if delta_content:
                    yield f"{delta_content}".encode('utf-8')
            yield b"__COMPLETE__"  # 发送特殊标志，表示测试已完成


@app.route('/role_match_send_message', methods=['POST'])
@jwt_required()
def role_match_send_message():
    global answers
    data = request.get_json()
    message = data.get('message')
    restart = data.get('restart', False)

    if restart:
        answers = []
        return jsonify({"message": "restart"})

    if message is not None:
        app.logger.debug(len(answers))
        if len(answers) < len(questions):
            answers.append(message)
            return Response(generate_role_match_stream(), content_type='text/event-stream')
        else:
            answers = []
            return jsonify({"message": "finish"})
    else:
        return jsonify({"error": "No message provided"}), 400


if __name__ == '__main__':
    app.run(debug=True)
