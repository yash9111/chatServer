from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# A dictionary to simulate chat processing
chat_sessions = {}

# Middleware to check for API access key
@app.before_request
def before_request():
    if request.endpoint not in ('get_chat_id',):
        access_key = request.headers.get('x-api-access-key')
        if access_key != '1234567890abcdefghijklmnopqrstuvwxyz':
            return jsonify({'error': 'Unauthorized access'}), 403

# Endpoint to get chat ID
@app.route('/', methods=['GET'])
def get_chat_id():
    chat_id = str(uuid.uuid4())
    chat_sessions[chat_id] = []
    return jsonify({'id': chat_id})

# Endpoint to process query
@app.route('/process', methods=['POST'])
def process_query():
    chat_id = request.headers.get('chat-id')
    if not chat_id or chat_id not in chat_sessions:
        return jsonify({'error': 'Invalid or missing chat ID'}), 400

    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400

    # Simulate processing query
    response_text = f"Processed query: {query}"
    chat_sessions[chat_id].append(query)
    return jsonify({'res': response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
