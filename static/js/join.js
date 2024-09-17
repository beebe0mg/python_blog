document.addEventListener('DOMContentLoaded', function() {
    // 파일 선택 입력 필드에서 파일이 선택될 때 발생하는 이벤트 리스너
    document.getElementById('fileInput').addEventListener('change', function (event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            const previewImage = document.getElementById('Preview-Image');
            previewImage.src = e.target.result;

            document.getElementById('Preview-Container').style.display = 'block';
            document.querySelector('label[for="fileInput"]').style.display = 'none';
            document.querySelectorAll('.Text-Container, .Input-Container, .Button-Container').forEach(function (section) {
                section.style.display = 'none';
            });
        };

        if (file) {
            reader.readAsDataURL(file);
        }
    });

    // 확인 버튼 클릭 시 실행되는 이벤트 리스너
    document.getElementById('Confirm-Button').addEventListener('click', function () {
        const completionContainer = document.getElementById('Completion-Container');
        completionContainer.style.display = 'flex';

        document.getElementById('Preview-Container').style.display = 'none';
        const label = document.querySelector('label[for="fileInput"]');
        label.style.display = 'none';

        label.parentNode.insertBefore(completionContainer, label);

        document.querySelectorAll('.Text-Container, .Input-Container, .Button-Container').forEach(function (section) {
            section.style.display = 'flex';
        });
    });
});
