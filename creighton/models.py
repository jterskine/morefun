from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
  
  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
    
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

class Posts(db.Model):
  __tablename__ = 'posts'
  uid = db.Column(db.Integer, primary_key = True)
  posttitle = db.Column(db.String(80))
  price = db.Column(db.Integer(80))
  email = db.Column(db.String(80))
  description = db.Column(db.String(180))
  
  
  def __init__(self, posttitle, price, email, description):
    self.posttitle = posttitle.title()
    self.price = price.title()
    self.email = email.lower()
    self.description = description.title()

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    subject = db.Column(db.String(80))
    author = db.Column(db.String(80))
    description = db.Column(db.String(80))
    pub_date = db.Column(db.Date)

    def __init__(
        self,
        title,
        author,
        description,
        subject,
        ):
        self.title = title
        self.author = author
        self.description = description
        self.subject = subject
        self.pub_date = datetime.now()
    
    
  
