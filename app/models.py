from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import uuid
db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    name = db.Column(db.String(150), nullable = True, default='')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref = 'userref', lazy = True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.token = secrets.token_hex(16)
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'token': self.token,
            'date_created': self.date_created
        }
        
    

class Character(db.Model):
    
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    name = db.Column(db.String(150), nullable = True, default='')
    description = db.Column(db.String(150), nullable = False)
    comics_appeared_in = db.Column(db.Integer, nullable = False)
    power = db.Column(db.String, default = '', unique = False )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self, name, description, comics, power, owner_id):
        self.name = name
        self.description= description
        self.comics_appeared_in = comics
        self.power = power
        self.owner = owner_id
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def save_changes(self):
        db.session.commit()
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    def to_dict(self):
        return {
            'id':self.id,
            'name': self.name,
            'description': self.description,
            'comics_appeared_in': self.comics_appeared_in,
            'power': self.power,
            'date_created': self.date_created
        }
    
    



# - id (Integer)
# - name (String)
# - description (String)
# - comics_appeared_in (Integer)
# - super_power (String)
# - date_created (DateTime w/ datetime.utcnow)
# - owner (FK to User using the user's token)