# clear_db.py
from app import app, db
from app import User, Post

with app.app_context():
    # 모든 User 및 Post 레코드 삭제
    User.query.delete()
    Post.query.delete()  # 모든 Post 레코드 삭제
    db.session.commit()