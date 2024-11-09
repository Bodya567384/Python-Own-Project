from crypt import methods
from pyexpat.errors import messages
from werkzeug.security import check_password_hash
from flask import Flask, request, session, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

SESSION_USER_ID = 'user_id'

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'retro.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET KEY'] = 'wO68AEm3cSknDmKt2ofLvx2yJwN_vf9wxzhU3geUeZs'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    role = db.Column(db.Integer(), default=0, nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Retro(db.Model):
    __tablename__ = 'Retro'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.Date(), default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=0)



with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/retro')
def retro():
    page = request.args.get('page', 1, type=int)
    list_retro = Retro.query.paginate(page=page, per_page=6)

    for item in list_retro:
        if len(item.text) > 200:
            item.text = item.text[:200] + ' ...'

    return render_template('retro.html', list_retro=list_retro)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            message = 'Invalid Email'
        else:
            if user.check_password(password):
                session[SESSION_USER_ID] = user.id
                return redirect('/')

            message = 'Invalid Password'

    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop(SESSION_USER_ID, None)
    return redirect('/')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/sidebar-right')
def sidebar():
    return render_template('index.html')


if __name__ == '__main__':
    app. run(debug=True)
