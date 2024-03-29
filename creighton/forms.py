from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, StringField, SelectField
from models import db, User
from flask_wtf.file import FileField

class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")

# class SellForm(Form):
#   title = TextField("Title",  [validators.Required("Please enter the title of item.")])
#   email = TextField("Email",  [validators.Required("Please enter your contact email address."), validators.Email("Please enter your contact email address.")])
#   isbn = TextField("ISB Number",  [validators.Required("Please enter a isb.")])
#   price = TextField("Price",  [validators.Required("Please enter a price.")])
#   # condition = TextAreaField("Condition",  [validators.Required("Please enter a description.")])
#   description = TextAreaField("Description",  [validators.Required("Please enter a description.")])
#   submit = SubmitField("Send")

class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True

class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
  
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    user = User.query.filter_by(email = self.email.data).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False



# from flask_wtf import Form
# from wtforms import validators, TextAreaField, StringField, SelectField


class NotesForm(Form):
    subject_list = [('0', 'English'), ('1', 'Philosophy'), ('2',
                    'Theology'), ('3', 'Mathematics')]
    title = StringField('Title', validators=[validators.Required()])
    author = StringField('Author', validators=[validators.Required()])
    description = TextAreaField('Description', validators=[validators.Required()])
    subject = SelectField(choices=subject_list)

class SellForm(Form):
  posttitle = TextField("Title",  [validators.Required("Please enter the title of item.")])
  price = TextField("Price",  [validators.Required("Please enter a price.")])
  email = TextField("Email",  [validators.Required("Please enter your contact email address."), validators.Email("Please enter your contact email address.")])
  description = TextAreaField("Description",  [validators.Required("Please enter a description.")])
  submit = SubmitField("Post")

class PhotoForm(Form):
    photo = FileField('Your photo')