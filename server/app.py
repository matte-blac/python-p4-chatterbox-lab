from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = db.session.query(Message).order_by(Message.created_at).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(
        body = data.get('body'),
        username = data.get('username'),
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow()
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def updated_messages(id):
    data = request.get_json()
    message = db.session.get(Message, id)
    if message is None:
        return jsonify({'error': 'Message not found'}), 404
    if 'body' in data:
        message.body = data['body']
        message.updated_at = datetime.utcnow()
        db.session.commit()
    return jsonify(message.to_dict())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_messages(id):
    message = db.session.get(Message, id)
    if message is None:
        return jsonify({'error': 'Message not found'}), 404
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5555)
