from app import db
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=True)
    tel = db.Column(db.String(10), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        f"User('{self.fullname}', '{self.email}', '{self.tel}')"



class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=True)
    tel = db.Column(db.String(10), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        f"User('{self.fullname}', '{self.email}', '{self.tel}')"

        
