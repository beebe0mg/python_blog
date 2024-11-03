from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
from flask_migrate import Migrate
from datetime import datetime

# 환경 변수 로드
load_dotenv()

# Flask 애플리케이션 객체 생성
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # 시크릿 키 설정
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 현재 파일 경로
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')  # 업로드 폴더 경로
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # 데이터베이스 URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')

# 업로드 폴더가 없으면 생성
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# SQLAlchemy 객체 생성
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 허용된 파일 확장자
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 데이터베이스 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID
    username = db.Column(db.String(150), nullable=False, unique=True)  # 사용자 이름
    email = db.Column(db.String(150), nullable=False, unique=True)  # 이메일
    password = db.Column(db.String(150), nullable=False)  # 비밀번호

# 데이터베이스 모델 정의
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)  # 이 줄이 추가되었는지 확인
    image_filename = db.Column(db.String(200))
    hashtags = db.Column(db.String(500))
    color = db.Column(db.String(7), default='#000000')
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

# 파일 확장자 검사 함수
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 홈 페이지 라우트
@app.route('/')
def home():
    return render_template('home.html')  # 홈 템플릿 렌더링

# 시작 페이지 라우트
@app.route('/start')
def start():
    return render_template('start.html')  # 시작 템플릿 렌더링

# 글쓰기 페이지 라우트
@app.route('/write')
def write():
    return render_template('write.html')  # 글쓰기 템플릿 렌더링

# 메인 페이지 라우트
@app.route('/main')
def main():
    return render_template('main.html')  # 메인 템플릿 렌더링

# bloghome 라우트 수정
@app.route('/bloghome')
def bloghome():
    all_posts = Post.query.order_by(Post.id.desc()).all()
    posts_with_users = []
    for post in all_posts:
        user = User.query.get(post.user_id)
        posts_with_users.append({
            'post': post,
            'username': user.username if user else '알 수 없는 사용자',
            'comments': post.comments  # 댓글 정보 추가
        })
    return render_template('bloghome.html', posts=posts_with_users)

# 회원가입 페이지 및 처리 라우트
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # 비밀번호 체크
        if not password:
            flash("비밀번호를 입력해 주세요.")
            return redirect(url_for('join'))
        
        if len(password) < 6:
            flash("비밀번호는 6자리 이상이어야 합니다.")
            return redirect(url_for('join'))

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        # 사용자 확인
        if email_exists and username_exists:
            flash("이메일과 사용자 이름이 모두 이미 존재합니다. 다른 이메일과 사용자 이름을 사용해 주세요.")
        elif email_exists:
            flash("이메일이 이미 존재합니다. 다른 이메일을 사용해 주세요.")
        elif username_exists:
            flash("사용자 이름이 이미 존재합니다. 다른 사용자 이름을 사용해 주세요.")
        else:
            # 사용자 추가
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            
            # 새로 생성된 사용자로 로그인
            session['user_id'] = new_user.id
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
            session['user_id'] = user.id  # 세션에 사용자 ID 저장
            return redirect(url_for('write'))
        else:
            flash("이메일 또는 비밀번호가 올바르지 않습니다.", 'error')
    return render_template('login.html')
# 모든 사용자 목록을 확인하는 페이지 라우트
@app.route('/users')
def users():
    all_users = User.query.all()  # 모든 사용자 가져오기
    return render_template('users.html', users=all_users)  # 사용자 템플릿 렌더링

# 이미지 업로드 엔드포인트
@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files.get('file')
    filename = secure_filename(file.filename)  # 파일 이름 안전하게 만들기
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # 파일 경로
    file.save(filepath)  # 파일 저장

    # 이미지 크기 조정
    img = Image.open(filepath)
    img = img.resize((300, 300))  # 크기 조정
    img.save(filepath)  # 수정된 이미지 저장

    return jsonify({'filename': filename})  # JSON 응답

# 해시태그 추가 엔드포인트
@app.route('/add_hashtag', methods=['POST'])
def add_hashtag():
    hashtag = request.json.get('hashtag')
    if hashtag:
        latest_post = Post.query.order_by(Post.id.desc()).first()  # 최신 포스트 가져오기
        if latest_post:  # 최신 포스트가 존재하면
            if latest_post.hashtags:  # 해시태그가 있으면
                latest_post.hashtags += f" #{hashtag}"  # 추가
            else:  # 해시태그가 없으면
                latest_post.hashtags = f"#{hashtag}"  # 새로 추가
            db.session.commit()  # 변경 사항 커밋
            return jsonify({'message': '해시태그가 성공적으로 추가되었습니다.'})  # 성공 메시지
    return jsonify({'error': '해시태그가 비어 있습니다.'}), 400  # 오류 메시지

# 포스트 작성 엔드포인트
@app.route('/post', methods=['POST'])
def create_post():
    try:
        if 'user_id' not in session:
            return jsonify({'error': '로그인이 필요합니다.'}), 401

        content = request.json.get('content')
        hashtags = request.json.get('hashtags')
        images = request.json.get('images')
        color = request.json.get('color', '#000000')  # 기본값은 검정색

        if not content or not images:
            return jsonify({'error': '내용과 이미지를 모두 입력해주세요.'}), 400

        user_id = session['user_id']
        image_filenames = [os.path.basename(image) for image in images]
        new_post = Post(user_id=user_id, content=content, hashtags=hashtags, 
                        image_filename=', '.join(image_filenames), color=color)
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': '포스트가 성공적으로 작성되었습니다.', 'redirect': url_for('bloghome')})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'포스트 작성 중 오류 발생: {str(e)}')
        return jsonify({'error': '포스트 작성 중 오류가 발생했습니다. 다시 시도해 주세요.'}), 500

# 업로드된 이미지 확인 엔드포인트
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)  # 이미지 파일 전송

@app.route('/posts')
def view_posts():
    all_posts = Post.query.all()  # 모든 포스트 가져오기
    return render_template('posts.html', posts=all_posts)  # posts.html 템플릿 렌더링

# 댓글 작성 라우트 추가
@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': '로그인이 필요합니다.'}), 401
    
    content = request.json.get('content')
    if not content:
        return jsonify({'success': False, 'error': '댓글 내용을 입력해주세요.'}), 400
    
    user = User.query.get(session['user_id'])
    new_comment = Comment(content=content, user_id=user.id, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'username': user.username,
        'content': content
    })


# 애플리케이션 실행
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)  # 디버그 모드로 실행
