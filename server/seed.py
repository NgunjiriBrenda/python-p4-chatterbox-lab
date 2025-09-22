from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from models import db, Message  

app = Flask(__name__)
api = Api(app)

class MessagesResource(Resource):
    def get(self):
        """GET /messages: returns all messages ordered by created_at ascending"""
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([message.to_dict() for message in messages])
    
    def post(self):
        """POST /messages: creates a new message"""
        data = request.get_json()
        
      
        if not data.get('body'):
            return {'error': 'Message body is required'}, 400
        if not data.get('username'):
            return {'error': 'Username is required'}, 400
        
        try:
            message = Message(
                body=data['body'],
                username=data['username']
            )
            
            db.session.add(message)
            db.session.commit()
            
            return jsonify(message.to_dict()), 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class MessageByIdResource(Resource):
    def patch(self, id):
        """PATCH /messages/<int:id>: updates message body"""
        message = db.session.get(Message, id)
        
        if not message:
            return {'error': 'Message not found'}, 404
        
        data = request.get_json()
        
        if not data.get('body'):
            return {'error': 'Message body is required'}, 400
        
        try:
            message.body = data['body']
            db.session.commit()
            
            return jsonify(message.to_dict())
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
    
    def delete(self, id):
        """DELETE /messages/<int:id>: deletes a message"""
        message = db.session.get(Message, id)
        
        if not message:
            return {'error': 'Message not found'}, 404
        
        try:
            db.session.delete(message)
            db.session.commit()
            
            return '', 204 
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500


api.add_resource(MessagesResource, '/messages')
api.add_resource(MessageByIdResource, '/messages/<int:id>')