import json
import os
from datetime import datetime
from flask import Flask, send_from_directory, jsonify, request, abort

app = Flask(__name__, static_folder='.')

SECRET_KEY = os.environ.get('UPDATE_SECRET', 'changeme')


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/content.json')
def content():
    return send_from_directory('.', 'content.json')


@app.route('/api/content', methods=['POST'])
def update_content():
    key = request.args.get('key') or request.headers.get('X-Update-Key')
    if key != SECRET_KEY:
        abort(403)
    data = request.get_json(force=True)
    if not data:
        abort(400)
    path = os.path.join(os.path.dirname(__file__), 'content.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({'ok': True, 'updated': data.get('updated')})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8765))
    app.run(host='0.0.0.0', port=port)
