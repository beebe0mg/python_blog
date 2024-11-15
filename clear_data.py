from app import app, db, Post, User, Comment

def clear_data():
    with app.app_context():
        # Comment 테이블의 모든 데이터 삭제
        num_comments = Comment.query.delete()
        
        # Post 테이블의 모든 데이터 삭제
        num_posts = Post.query.delete()
        
        # User 테이블의 모든 데이터 삭제
        num_users = User.query.delete()
        
        # 변경사항 커밋
        db.session.commit()
        
        print(f"{num_comments}개의 댓글, {num_posts}개의 포스트, {num_users}명의 사용자 데이터가 삭제되었습니다.")

if __name__ == '__main__':
    clear_data()