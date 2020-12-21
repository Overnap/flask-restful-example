from database import db
from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(100))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password.encode('utf-8')).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    uploader = db.Column(db.String(45))
    address = db.Column(db.String(50), unique=True)
    contact = db.Column(db.String(50))
    introduction = db.Column(db.String(200))
    latitude = db.Column(db.FLOAT())
    longitude = db.Column(db.FLOAT())

    def __init__(self, uploader, address, contact, introduction, latitude, longitude):
        self.uploader = uploader
        self.address = address
        self.contact = contact
        self.introduction = introduction
        self.latitude = latitude
        self.longitude = longitude
