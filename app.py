from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sabrinasultana5115@gmail.com'
app.config['MAIL_PASSWORD'] = 'Mahfujur$51'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask_blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Contacts(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    number = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route("/")
def home():
    blogname = "TechBlog"
    tag_line = "Your Dream start form here"
    fb_url = "https://www.facebook.com/mahfujur.just"
    return render_template('index.html', name=blogname, tag_line=tag_line, fb=fb_url)


@app.route("/posts/<string:post_slug>")
def post(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',post=post)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        number = request.form.get('number')
        message = request.form.get('message')
        entry = Contacts(name=name, number=number, message=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        msg = Message('Hello', sender=email, recipients=['sabrinasultana5115@gmail.com'])
        msg.body = message
        mail.send(msg)
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
