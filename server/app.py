from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

@app.route('/')
def index():
    return 'Chatterbox API'

# GET /messages - returns all messages ordered by created_at ascending
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

# POST /messages - creates a new message
@app.route('/messages', methods=['POST'])
def create_message():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('body') or not data.get('username'):
            return jsonify({'error': 'Body and username are required'}), 400
        
        # Create new message
        new_message = Message(
            body=data['body'],
            username=data['username']
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify(new_message.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# PATCH /messages/<int:id> - updates a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    try:
        message = Message.query.get(id)
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        data = request.get_json()
        
        # Update the message body if provided
        if 'body' in data:
            message.body = data['body']
        
        db.session.commit()
        
        return jsonify(message.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# DELETE /messages/<int:id> - deletes a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    try:
        message = Message.query.get(id)
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        db.session.delete(message)
        db.session.commit()
        
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)