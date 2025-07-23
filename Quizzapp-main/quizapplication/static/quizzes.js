document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/quizzes/')
    .then(res => res.json())
    .then(data => {
      const list = document.getElementById('quizList');
      data.forEach(quiz => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
          <div>
            <strong>${quiz.title}</strong><br/>
            ${quiz.description}
          </div>
          <a href="/quiz/${quiz.id}/start/" class="btn btn-primary">Start Quiz</a>
        `;
        list.appendChild(li);
      });
    });
});
