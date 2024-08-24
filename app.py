from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    message=db.relationship('Message',backref='user',lazy=True)
    def __repr__(self):
        return f'<User {self.name}>'
class Message(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.Text)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    def __repr__(self):
        return f'<Message {self.text}>'
@app.route('/users',methods=['POST'])
def create_user():
    data=request.get_json()
    if User.query.filter_by(name=data['name']).first():
        return jsonify({'message':'User already exists'}),409
    new_user=User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'User created'})
@app.route('/users',methods=['GET'])
def get_users():
    users=User.query.all()
    output=[]
    for user in users:
        user_data={"id":user.id,'name':user.name}
        output.append(user_data)
    return jsonify({'users':output})
@app.route('/messages',methods=['POST'])
def create_message():
    data=request.get_json()
    user=User.query.filter_by(name=data['name']).first()
    if not user:
        return jsonify({'message':'User does not exist'}),400
    new_message=Message(text=data['text'],user_id=user.id)
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message':'Message created'})
@app.route('/messages',methods=['GET'])
def get_messages():
    messages=Message.query.all()
    output=[]
    for message in messages:
        message_data={"id":message.id,'text':message.text,'name':message.user.name}
        output.append(message_data)
    return jsonify({'messages':output})
if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=True)