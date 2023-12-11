from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()



roles_users=db.Table('roles_users', 
                     db.Column('user_id', db.Integer(), db.ForeignKey('user.user_id')),
                     db.Column('role_id', db.Integer(), db.ForeignKey('role.role_id')))



class User(db.Model,UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True, nullable = False)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    role_id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(80), unique=True)
    
    
  
class Hall(db.Model):
    __tablename__ = 'hall'
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)
    hall_id = db.Column(db.Integer, autoincrement = True, unique=True, primary_key=True)
    hall_name = db.Column(db.String)
    place = db.Column(db.String)
    size = db.Column(db.Integer)
    

class Shows(db.Model):
    __tablename__ = "shows"
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)
    hall_id = db.Column(db.Integer, db.ForeignKey("hall.hall_id"))
    show_id = db.Column(db.Integer, autoincrement = True, unique=True, primary_key=True)
    show_name = db.Column(db.String, nullable = False)
    about = db.Column(db.String, nullable = False)
    genre = db.Column(db.String, nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    time = db.Column(db.String, nullable = False)
    left_seat=db.Column(db.Integer, db.ForeignKey("hall.size"))
    ticketPrice = db.Column(db.Integer, nullable=False)


class Bookings(db.Model):
    booking_id = db.Column(db.Integer, autoincrement = True, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)
    hall_id = db.Column(db.Integer, db.ForeignKey("hall.hall_id"))
    show_id = db.Column(db.Integer, db.ForeignKey("shows.show_id"))
    hall_name = db.Column(db.String, db.ForeignKey("hall.hall_name"))
    place = db.Column(db.String, db.ForeignKey("hall.place"))
    show_name = db.Column(db.String, db.ForeignKey("shows.show_id"))
    time = db.Column(db.String, db.ForeignKey("shows.time"))
    n_tickets = db.Column(db.Integer, nullable=False)
    ticketPrice=db.Column(db.Integer, db.ForeignKey("shows.ticketPrice"))
    total_price= db.Column(db.Integer, nullable=False)