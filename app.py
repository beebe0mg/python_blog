from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image

# 환경 변수 로드
load_dotenv()

# Flask 애플리케이션 객체 생성
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# SQLAlchemy 객체 생성
db = SQLAlchemy(app)

# 허용된 파일 확장자
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 데이터베이스 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(200))
    hashtags = db.Column(db.String(500))

with app.app_context():
    db.create_all()

# 파일 확장자 검사
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 홈 페이지 라우트
@app.route('/')
def home():
    return render_template('home.html')

# 시작 페이지 라우트
@app.route('/start')
def start():
    return render_template('start.html')

# 글쓰기 페이지 라우트
@app.route('/write')
def write():
    return render_template('write.html')

# 메인 페이지 라우트
@app.route('/main')
def main():
    return render_template('main.html')

# 회원가입 페이지 및 처리 라우트
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not password:
            flash("비밀번호를 입력해 주세요.")
            return redirect(url_for('join'))
        
        if len(password) < 6:
            flash("비밀번호는 6자리 이상이어야 합니다.")
            return redirect(url_for('join'))

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists and username_exists:
            flash("이메일과 사용자 이름이 모두 이미 존재합니다. 다른 이메일과 사용자 이름을 사용해 주세요.")
        elif email_exists:
            flash("이메일이 이미 존재합니다. 다른 이메일을 사용해 주세요.")
        elif username_exists:
            flash("사용자 이름이 이미 존재합니다. 다른 사용자 이름을 사용해 주세요.")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('write'))

        return redirect(url_for('join'))

    return render_template('join.html')

# 로그인 페이지 및 처리 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            flash("성공적으로 로그인되었습니다.", 'success')
            return redirect(url_for('write'))
        else:
            flash("이메일 또는 비밀번호가 올바르지 않습니다.", 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

# 모든 사용자 목록을 확인하는 페이지 라우트
@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

# 이미지 업로드 엔드포인트
@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files.get('file')
    if not file or not allowed_file(file.filename):
        return jsonify({'error': '올바른 파일을 선택해 주세요.'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # 이미지 크기 조정
    img = Image.open(filepath)
    img = img.resize((300, 300))
    img.save(filepath)

    # DB에 이미지 파일명 저장
    new_post = Post(image_filename=filename)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'filename': filename})

# 해시태그 추가 엔드포인트
@app.route('/add_hashtag', methods=['POST'])
def add_hashtag():
    hashtag = request.json.get('hashtag')
    if hashtag:
        latest_post = Post.query.order_by(Post.id.desc()).first()
        latest_post.hashtags = (latest_post.hashtags or '') + f" #{hashtag}"
        db.session.commit()
        return jsonify({'message': '해시태그가 성공적으로 추가되었습니다.'})
    return jsonify({'error': '해시태그가 비어 있습니다.'}), 400

# 업로드된 이미지 확인 엔드포인트
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)
