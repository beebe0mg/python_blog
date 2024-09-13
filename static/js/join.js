// 파일 선택 입력 필드에서 파일이 선택될 때 발생하는 이벤트 리스너
document.getElementById('fileInput').addEventListener('change', function (event) {
    // 선택된 파일을 가져옴
    const file = event.target.files[0];
    // FileReader 객체를 생성하여 파일을 읽을 준비
    const reader = new FileReader();

    // 파일이 성공적으로 읽혀졌을 때 호출되는 이벤트 핸들러
    reader.onload = function (e) {
        // 이미지 미리보기 요소를 가져옴
        const previewImage = document.getElementById('Preview-Image');
        // FileReader가 읽은 파일의 데이터 URL을 미리보기 이미지의 src에 설정
        previewImage.src = e.target.result;

        // 미리보기 컨테이너를 보여줌
        document.getElementById('Preview-Container').style.display = 'block';

        // 파일 선택 버튼(label)을 숨김
        document.querySelector('label[for="fileInput"]').style.display = 'none';

        // 텍스트, 입력 필드, 회원가입 버튼 섹션을 숨김
        document.querySelectorAll('.Text-Container, .Input-Container, .Button-Container').forEach(function (section) {
            section.style.display = 'none';
        });
    };

    // 파일이 선택된 경우에만 읽기 시작
    if (file) {
        reader.readAsDataURL(file); // 파일을 읽어 Data URL로 변환
    }
});

// 확인 버튼 클릭 시 실행되는 이벤트 리스너
document.getElementById('Confirm-Button').addEventListener('click', function () {
    // 완료 메시지 컨테이너를 보여줌
    const completionContainer = document.getElementById('Completion-Container');
    completionContainer.style.display = 'flex';

    // 이미지 미리보기 컨테이너를 숨김
    document.getElementById('Preview-Container').style.display = 'none';

    // 파일 선택 버튼(label)을 다시 숨김
    const label = document.querySelector('label[for="fileInput"]');
    label.style.display = 'none';

    // 완료 메시지를 label이 있던 자리에 삽입
    label.parentNode.insertBefore(completionContainer, label);

    // 숨겨졌던 섹션(텍스트, 입력 필드, 회원가입 버튼)을 다시 보이도록 설정
    document.querySelectorAll('.Text-Container, .Input-Container, .Button-Container').forEach(function (section) {
        section.style.display = 'flex'; // 섹션들을 다시 보이게 설정
    });
});
