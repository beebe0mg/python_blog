document.querySelectorAll('.comment-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const postId = this.dataset.postId;
        const content = this.querySelector('textarea').value;
        const commentsSection = this.closest('.comments-section');
        
        fetch(`/post/${postId}/comment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: content })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 새 댓글을 화면에 추가
                const commentsList = commentsSection.querySelector('.comments-list');
                const newComment = document.createElement('div');
                newComment.className = 'comment';
                newComment.innerHTML = `<p><strong>${data.username}</strong>: ${data.content}</p>`;
                commentsList.appendChild(newComment);
                
                // 입력 필드 초기화
                this.querySelector('textarea').value = '';
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});