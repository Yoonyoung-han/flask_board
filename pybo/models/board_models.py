from pybo.handlers.mongo import Mongo
import datetime

mongo = Mongo()
db = mongo.get_db()

class User(db.Document):
    id = db.ObjectIdField(primary_key=True, comment='_id',EmbeddedDocumentField=True)
    username = db.StringField(unique=True,required= True, comment='username')
    password = db.StringField(required= True, comment='password')
    email = db.EmailField(unique=True, required= True, comment='email')

class Question(db.Document):
    id = db.ObjectIdField(primary_key=True, comment='_id')
    subject = db.StringField(max_length=200, required= True, comment='subject')
    content = db.StringField(required= True, comment='content')
    create_date = db.DateTimeField(default=datetime.datetime.now, comment='create_date')
    user_id = db.ReferenceField(User,reverse_delete_rule= db.CASCADE, comment='user_id', server_default='1')
    user = db.ReferenceField(User, comment='user')
    modify_date = db.DateTimeField(comment='modify_date')
    voter = db.ListField(comment='voter')

class Answer(db.Document):
    id = db.ObjectIdField(primary_key=True, comment='_id')
    question_id = db.ReferenceField(Question,reverse_delete_rule= db.CASCADE, comment='question_id') #CASCADE
    content = db.StringField(required= True, comment='content')
    create_date = db.DateTimeField(default=datetime.datetime.now, comment='create_date')
    user_id = db.ReferenceField(User,reverse_delete_rule= db.CASCADE, comment='user_id', server_default='1')
    user = db.ReferenceField(User, comment='user')
    modify_date = db.DateTimeField(comment='modify_date')
    voter = db.ListField(comment='voter')

class Comment(db.Document):
    id = db.ObjectIdField(primary_key=True, comment='_id')
    user_id = db.ReferenceField(User,on_delete= db.CASCADE, comment='user_id',required=True)
    user = db.ReferenceField(User, comment='user')
    content = db.StringField(required= True, comment='content')
    create_date = db.DateTimeField(default=datetime.datetime.now, comment='create_date')
    modify_date = db.DateTimeField(comment='modify_date')
    question_id = db.ReferenceField(Question,on_delete= db.CASCADE, comment='question_id')
    answer_id = db.ReferenceField(Answer, on_delete= db.CASCADE, comment='answer_id')