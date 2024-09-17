from app import app, db

with app.app_context():
    db.create_all()  # 데이터베이스와 테이블 생성
