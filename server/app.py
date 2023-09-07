from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        return jsonify([message.serialize() for message in messages])

    elif request.method == 'POST':
        data = request.json
        new_message = Message(body=data['body'], username=data['username'], created_at=datetime.utcnow())
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.serialize()), 201

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)

    if not message:
        return make_response(jsonify({'error': 'Message not found'}), 404)

    if request.method == 'GET':
        return jsonify(message.serialize())

    elif request.method == 'PATCH':
        data = request.json
        message.body = data['body']
        db.session.commit()
        return jsonify(message.serialize())

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted'})

def serialize(self):
    return {
        'id': self.id,
        'body': self.body,
        'username': self.username,
        'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }



if __name__ == '__main__':
    app.run(port=5555)
