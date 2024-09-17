from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 비밀 키 설정
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# 절대 경로 설정
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # 비밀번호 입력 확인
        if not password:
            flash("비밀번호를 입력해 주세요.")
            return redirect(url_for('join'))
        
        # 비밀번호 길이 확인
        if len(password) < 6:
            flash("비밀번호는 6자리 이상이어야 합니다.")
            return redirect(url_for('join'))
        
        # 중복 이메일 확인
        email_exists = User.query.filter_by(email=email).first()
        
        # 중복 사용자 이름 확인
        username_exists = User.query.filter_by(username=username).first()
        
        # 중복 이메일과 사용자 이름에 대한 메시지 처리
        if email_exists and username_exists:
            flash("이메일과 사용자 이름이 모두 이미 존재합니다. 다른 이메일과 사용자 이름을 사용해 주세요.")
        elif email_exists:
            flash("이메일이 이미 존재합니다. 다른 이메일을 사용해 주세요.")
        elif username_exists:
            flash("사용자 이름이 이미 존재합니다. 다른 사용자 이름을 사용해 주세요.")
        else:
            # 사용자 데이터베이스에 저장
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('home'))
        
        return redirect(url_for('join'))
    
    return render_template('join.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/users')
def users():
    all_users = User.query.all()  # 모든 사용자 정보를 가져옴
    return render_template('users.html', users=all_users)

if __name__ == '__main__':
    app.run(debug=True)
