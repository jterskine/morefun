import os
from creighton import app
from flask import render_template, request, flash, session, url_for, redirect, send_from_directory
from forms import ContactForm, SignupForm, SigninForm, SellForm #NotesForm
from flask.ext.mail import Message, Mail
from models import db, User, Posts #Notes
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


mail = Mail()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/')
def home():
  posts = Posts.query.all()
  return render_template('home.html', posts=posts)


# def home():
#   notes = Notes.query.all()
#   return render_template('home.html', notes=notes)

@app.route('/purpose')
def purpose():
  return render_template('purpose.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='joeterskine@gmail.com', recipients=['joeterskine@gmail.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)

      return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if 'email' in session:
    return redirect(url_for('profile')) 
  
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      
      session['email'] = newuser.email
      return redirect(url_for('profile'))
  
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/profile')
def profile():

  if 'email' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(email = session['email']).first()

  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if 'email' in session:
    return redirect(url_for('profile')) 
      
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))
                
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():

  if 'email' not in session:
    return redirect(url_for('signin'))
    
  session.pop('email', None)
  return redirect(url_for('home'))


@app.route('/posts/')
def list_posts():
    posts = Posts.query.all()
    return render_template('home.html', posts=posts)

@app.route('/posts/create/', methods=['GET', 'POST'])
def createPost():
    form = SellForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Posts(form.posttitle.data, form.price.data,
                         form.email.data, form.description.data)
            db.session.add(post)
            db.session.commit()
            #flash('Post saved on database.')
            return redirect(url_for('list_posts'))
    return render_template('post.html', form=form)


@app.route('/posts/delete/<int:post_uid>', methods=['GET'])
def deletePost(post_uid):
    post = Posts.query.get_or_404(post_uid)
    db.session.delete(post)
    db.session.commit()
    #flash('post Deleted')
    return redirect(url_for('list_posts'))


@app.route('/posts/edit/<int:post_uid>', methods=['GET', 'POST'])
def editPost(post_uid):
    post = Posts.query.get_or_404(post_uid)
    form = SellForm(obj=post)
    if request.method == 'POST':
        print request.form
        if form.validate_on_submit():
            print request.form['posttitle']
            post.posttitle = request.form['posttitle']
            post.price = request.form['price']
            post.email = request.form['email']
            post.description = request.form['description']
            db.session.add(post)
            db.session.commit()
            #flash('post editted')
        return redirect(url_for('list_posts'))
    else:
        return render_template('post.html', form=form)




# @app.route('/notes/')
# def list_notes():
#     notes = Notes.query.all()
#     return render_template('home.html', notes=notes)


# @app.route('/notes/create/', methods=['GET', 'POST'])
# def create():
#     form = SellForm()
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             post = Posts(form.title.data, form.author.data,
#                          form.description.data, form.subject.data)
#             db.session.add(post)
#             db.session.commit()
#             # flash('Note saved on database.')
#             return redirect(url_for('list_notes'))
#     return render_template('note.html', form=form)

# @app.route('/notes/delete/<int:note_id>', methods=['GET'])
# def delete(note_id):
#     note = Notes.query.get_or_404(note_id)
#     db.session.delete(note)
#     db.session.commit()
#     flash('Note Deleted')
#     return redirect(url_for('list_notes'))

# @app.route('/notes/edit/<int:note_id>', methods=['GET', 'POST'])
# def edit(note_id):
#     note = Notes.query.get_or_404(note_id)
#     form = NotesForm(obj=note)
#     if request.method == 'POST':
#         print request.form
#         if form.validate_on_submit():
#             print request.form['title']
#             note.title = request.form['title']
#             note.author = request.form['author']
#             note.description = request.form['description']
#             note.subject = request.form['subject']
#             db.session.add(note)
#             db.session.commit()
#         return redirect(url_for('list_notes'))
#     else:
#         return render_template('note.html', form=form)
# @app.route('/sell', methods=['GET', 'POST'])
# def sell():
#   form = SellForm()

#   if request.method == 'POST':
#     if form.validate() == False:
#       flash('All fields are required.')
#       return render_template('sell.html', form=form)
#     else:
#       # msg = Message(form.subject.data, sender='joeterskine@gmail.com', recipients=['joeterskine@gmail.com'])
#       # msg.body = """
#       # From: %s <%s>
#       # %s
#       # """ % (form.name.data, form.email.data, form.message.data)
#       # mail.send(msg)
#       return render_template('sell.html', success=True)

#   elif request.method == 'GET':
#     return render_template('sell.html', form=form)

# @app.route('/posts')
# def posts():
#   form = SignupForm

#   if 'email' in session:
#     return redirect(url_for('sell')) 
  
#   if request.method == 'POST':
#     if form.validate() == False:
#       return render_template('sell.html', form=form)
#     else:
#       newpost = Post(form.posttitle.data, form.isbn.data, form.price.data, form.email.data)
#       db.session.add(newpost)
#       db.session.commit()
      
#       session['email'] = newpost.email
#       return redirect(url_for('profile'))
  
#   elif request.method == 'GET':
#     return render_template('signup.html', form=form)

# @app.route('/display')
# def redirect_to_home():
#     return redirect(url_for('list_notes'))

