document.addEventListener('DOMContentLoaded', () => {
  const quizId = document.getElementById("quizForm").dataset.quizId;
  let timeLimit = 60;
  let interval = null;

  // Load questions
  fetch(`/api/quiz/${quizId}/questions/`)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById('questionContainer');
      data.forEach((q, index) => {
        const block = document.createElement('div');
        block.innerHTML = `
          <p><strong>Q${index + 1}:</strong> ${q.text}</p>
          ${[1, 2, 3, 4].map(i => `
            <div class="form-check">
              <input class="form-check-input" type="radio" name="q${q.id}" value="${i}">
              <label class="form-check-label">${q['option' + i]}</label>
            </div>
          `).join('')}
          <hr>
        `;
        container.appendChild(block);
      });
    });

  // Load timer
  fetch('/api/quizzes/')
    .then(res => res.json())
    .then(data => {
      const quiz = data.find(q => q.id == quizId);
      timeLimit = quiz.time_limit || 60;
      let time = timeLimit;
      const timerDiv = document.getElementById("timer");

      interval = setInterval(() => {
        timerDiv.innerText = `${time} seconds left`;
        time--;
        if (time < 0) {
          clearInterval(interval);
          document.getElementById("quizForm").dispatchEvent(new Event('submit'));
        }
      }, 1000);
    });

  // Handle submission
  document.getElementById("quizForm").addEventListener("submit", function (e) {
    e.preventDefault();
    clearInterval(interval); //  Stop timer

    let answers = {};
    const inputs = document.querySelectorAll("input[type=radio]:checked");
    inputs.forEach(i => {
      const qid = i.name.slice(1);
      answers[qid] = parseInt(i.value);
    });

    fetch('/api/submit/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
      },
      body: JSON.stringify({
        quiz_id: quizId,
        answers: answers
      })
    })
      .then(res => res.json())
      .then(data => {
        const container = document.getElementById('questionContainer');
        container.innerHTML = ''; // Clear old content

        data.details.forEach((res, index) => {
          const isCorrect = res.selected && res.selected == res.correct;
          const block = document.createElement('div');
          block.innerHTML = `
            <p><strong>Q${index + 1}:</strong> ${res.question}</p>
            <p>Your Answer: Option ${res.selected || 'Not Answered'}</p>
            <p>Correct Answer: Option ${res.correct} - ${res.correct_option_text}</p>
            <div class="alert ${isCorrect ? 'alert-success' : 'alert-danger'}">
              ${isCorrect ? 'Correct ✅' : 'Incorrect ❌'}
            </div>
            <hr>
          `;
          container.appendChild(block);
        });

        const scoreBlock = document.createElement('div');
        scoreBlock.innerHTML = `
          <h4 class="mt-4">You scored ${data.score} out of ${data.details.length}</h4>
          <a href="/leaderboard/${quizId}/" class="btn btn-primary mt-3">View Leaderboard</a>
        `;
        container.appendChild(scoreBlock);

        //  Disable form elements to prevent re-submission
        document.querySelectorAll("input[type=radio]").forEach(input => input.disabled = true);
        document.querySelector("button[type=submit]").disabled = true;
      })
      .catch(error => {
        alert("There was an error submitting your quiz.");
        console.error(error);
      });
  });
});
