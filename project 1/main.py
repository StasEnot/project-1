from flask import Flask, request
from flask import render_template
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Games(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(255), nullable=False)
    post_text = db.Column(db.Text(), nullable=False)
    post_image = db.Column(db.String(255), nullable=False)
    studio = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.Date(), default=datetime.utcnow)
    def __init__(self, name, text, url, studio):
        self.post_name = name
        self.post_text = text
        self.post_image = url
        self.studio = studio

class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True)
    admin_login = db.Column(db.String(25), nullable=False)
    admin_password = db.Column(db.String(25), nullable=False)
    def __init__(self, login, password):
        self.admin_login = login
        self.admin_password = password


#with app.app_context():
#    db.drop_all()
 #   db.create_all()
  #  admin= Admin('root', 'root')
   # db.session.add(admin)
    #db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/Login', methods=['POST'])
def Admin_login():
    login = request.form['login']
    password = request.form['password']
    if Admin.query.filter_by(admin_login=login).all() == []:
        return render_template('login_admin.html')
    else:
        return render_template('add_game.html')

@app.route('/', methods=['GET'])
def add_game():
    title = request.form['title']
    text = request.form['text']
    URL = request.form['URL']
    studio = request.form['studio']
    row = Games(title, text, URL, studio)
    db.session.add(row)
    db.session.commit()
    return render_template('Top_games.html')


@app.route('/Top_games')
def Top_games():
    return render_template('Top_games.html')

if __name__ == '__main__':
    app.run()