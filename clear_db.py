# clear_db.py
from app import app, db
from app import User

with app.app_context():
    # 모든 User 레코드 삭제
    User.query.delete()
    db.session.commit()
