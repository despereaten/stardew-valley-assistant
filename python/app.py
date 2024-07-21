from flask import Flask, request, jsonify
from flask_cors import CORS
from RAGTest import get_response

import os

app = Flask(__name__)
CORS(app)


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    if user_message:
        ai_message = get_response(user_message)
        response = {"response": ai_message}
    else:
        response = {"response": "No message provided"}

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
