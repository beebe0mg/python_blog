from flask import Flask, render_template
# Flask 프레임워크에서 Flask 클래스와 render_template 함수를 임포트 한다.
# Flask 는 웹 애플리케이션을 생성하는 데 사용되는 주요 클래스이다.
# render_template 는 HTML 파일을 렌더링하여 웹 페이지를 생성하는 함수이다.

app = Flask(__name__)
# Flask 클래스의 객체를 생성하고 app 변수에 저장한다.
# __name__ 은 현재 모듈의 이름을 나타내는 파이썬 내장 변수이다.
# 6 번째 줄은 Flask 애플리케이션을 만드는 데 사용

@app.route('/')
# Flask 애플리케이션의 경로 정의, 루트 URL 을 의미함. 해당하는 주소에 접근했을 때 함수 호출됨.
def home():
    return render_template('home.html')
# render_template 함수로 home.html 파일을 렌더링 하여 생성

@app.route('/login')
# url_for('login')에서 'login'은 여기서 정의된 login 함수와 연결된 URL
def login():
    return render_template('login.html')

if __name__ == '__main__':
# 현재 모듈이 main일 때만 실행.
    app.run(debug=True)
# Flask 애플리케이션을 실행하는 명령
# debug=True 는 디버그 모드를 활성화하는 것임.