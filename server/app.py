from flask import Flask, request, jsonify
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    db.create_all()
    

    Message.query.delete()
    db.session.commit()
    
   
    messages = [
        Message(body="Hello world!", username="test_user"),
        Message(body="Testing 123", username="another_user"),
        Message(body="Flask is cool!", username="python_dev")
    ]
    
    db.session.add_all(messages)
    db.session.commit()
    print("✅ Database seeded with test messages!")

@app.route('/')
def home():
    return '<h1>Code Challenge</h1>'

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    
    if not data or not data.get('body'):
        return jsonify({'error': 'Message body is required'}), 400
    if not data.get('username'):
        return jsonify({'error': 'Username is required'}), 400
    
    try:
        message = Message(body=data['body'], username=data['username'])
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    data = request.get_json()
    if not data or not data.get('body'):
        return jsonify({'error': 'Message body is required'}), 400
    
    try:
        message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    try:
        db.session.delete(message)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)