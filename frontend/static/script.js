function renderActivity() {
  console.log('Rendering activity...');
  fetch('data/output.json')
    .then(response => response.json())
    .then(jsonData => {
      console.log(jsonData);
      document.querySelector('.image').innerHTML = `<img id="target_image" src="${jsonData.media.image_src}" alt="Image">`;
      document.getElementById('image_container').addEventListener('click', () => {
        window.open(jsonData.media.image_src, '_blank');
      });
      document.getElementById('sentence').textContent = `${jsonData.sentence}`;
      const trueSpan = document.querySelector('#options_container .true');
      const falseSpan = document.querySelector('#options_container .false');
      let sentence_div = document.getElementById('sentence_div');
      let sentence_span = document.getElementById('sentence');
      
      trueSpan.addEventListener('click', () => {
        const userChoice = trueSpan.textContent.trim().toUpperCase();
        const correctAnswer = jsonData.correct_answer.toUpperCase();

        if (userChoice === correctAnswer) {
          sentence_span.style.backgroundColor = '#8CC63F';
          sentence_span.style.color = 'white';
          sentence_div.marginLeft = '3vw';
          sentence_div.marginRight = '3vw';
        } else {
          sentence_span.style.backgroundColor = 'white';
          sentence_span.style.color = '#D32B45';
          sentence_span.style.textDecoration = 'line-through';
          sentence_div.marginLeft = '3vw';
          sentence_div.marginRight = '3vw';
        }
      });

      falseSpan.addEventListener('click', () => {
        const userChoice = falseSpan.textContent.trim().toUpperCase();
        const correctAnswer = jsonData.correct_answer.toUpperCase();

        if (userChoice === correctAnswer) {
          sentence_span.style.backgroundColor = '#8CC63F';
          sentence_span.style.color = 'white';
          sentence_div.marginLeft = '3vw';
          sentence_div.marginRight = '3vw';
        } else {
          sentence_span.style.backgroundColor = 'white';
          sentence_span.style.color = '#D32B45';
          sentence_span.style.textDecoration = 'line-through';
          sentence_div.marginLeft = '3vw';
          sentence_div.marginRight = '3vw';
        }
      });
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
}

function generateActivity() {
  const targetLevel = document.getElementById('target-level').value;
  const targetVocabulary = document.getElementById('target-vocabulary').value;
  const endpoint = '/generate-activity';
  const payload = {
    level: targetLevel,
    vocabulary: targetVocabulary
  };
  fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })
  .then(response => response.json())
  .then(data => {
    console.log('Activity generated. Response :', data);
    renderActivity();
  })
  .catch(error => {
    console.error('Error generating activity:', error);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('generate_activity_button').addEventListener('click', generateActivity);
  renderActivity();
});