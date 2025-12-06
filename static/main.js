// Enhanced Interview Bot Features
document.addEventListener('DOMContentLoaded', function() {
    // Auto-save answers to localStorage
    const answerTextarea = document.getElementById('answer');
    if (answerTextarea) {
        // Load saved answer
        const savedAnswer = localStorage.getItem('interview_answer');
        if (savedAnswer) {
            answerTextarea.value = savedAnswer;
        }

        // Save answer as user types
        answerTextarea.addEventListener('input', function() {
            localStorage.setItem('interview_answer', this.value);
        });
    }

    // Character counter for answers
    if (answerTextarea) {
        const charCounter = document.createElement('div');
        charCounter.className = 'char-counter';
        charCounter.innerHTML = `Characters: <span id="char-count">${answerTextarea.value.length}</span>`;
        answerTextarea.parentNode.insertBefore(charCounter, answerTextarea.nextSibling);

        answerTextarea.addEventListener('input', function() {
            document.getElementById('char-count').textContent = this.value.length;
        });
    }

    // Timer functionality
    let interviewTimer;
    let startTime;

    function startTimer() {
        startTime = Date.now();
        const timerDisplay = document.createElement('div');
        timerDisplay.id = 'timer';
        timerDisplay.className = 'timer';
        timerDisplay.innerHTML = 'Time: <span id="time-elapsed">00:00</span>';
        
        const container = document.querySelector('.container');
        const firstForm = container.querySelector('form');
        container.insertBefore(timerDisplay, firstForm);

        interviewTimer = setInterval(function() {
            const elapsed = Date.now() - startTime;
            const minutes = Math.floor(elapsed / 60000);
            const seconds = Math.floor((elapsed % 60000) / 1000);
            document.getElementById('time-elapsed').textContent = 
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);
    }

    // Start timer when question appears
    if (document.querySelector('.question') || answerTextarea) {
        startTimer();
    }

    // Clear saved answer when starting new interview
    const startButton = document.querySelector('button[type="submit"]');
    if (startButton && !answerTextarea) {
        startButton.addEventListener('click', function() {
            localStorage.removeItem('interview_answer');
        });
    }

    // Copy question to clipboard
    const questionElement = document.querySelector('.question');
    if (questionElement) {
        const copyButton = document.createElement('button');
        copyButton.type = 'button';
        copyButton.className = 'copy-btn';
        copyButton.textContent = '📋 Copy Question';
        copyButton.onclick = function() {
            navigator.clipboard.writeText(questionElement.textContent).then(function() {
                copyButton.textContent = '✅ Copied!';
                setTimeout(() => copyButton.textContent = '📋 Copy Question', 2000);
            });
        };
        questionElement.appendChild(copyButton);
    }

    // Difficulty level tips
    const difficultySelect = document.getElementById('difficulty');
    if (difficultySelect) {
        const tipsDiv = document.createElement('div');
        tipsDiv.className = 'difficulty-tips';
        difficultySelect.parentNode.insertBefore(tipsDiv, difficultySelect.nextSibling);

        difficultySelect.addEventListener('change', function() {
            const tips = {
                'easy': 'Perfect for beginners! Focus on basic concepts and syntax.',
                'medium': 'Good for intermediate level. Expect problem-solving questions.',
                'hard': 'Advanced level. Prepare for complex algorithms and system design.'
            };
            tipsDiv.innerHTML = `<small class="tip">💡 ${tips[this.value]}</small>`;
        });
    }
});

// Speech-to-text functionality (if supported)
function startSpeechRecognition() {
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        const answerTextarea = document.getElementById('answer');
        if (answerTextarea) {
            const speechButton = document.createElement('button');
            speechButton.type = 'button';
            speechButton.className = 'speech-btn';
            speechButton.innerHTML = '🎤 Voice Input';
            answerTextarea.parentNode.insertBefore(speechButton, answerTextarea.nextSibling);

            speechButton.onclick = function() {
                if (speechButton.textContent.includes('🎤')) {
                    recognition.start();
                    speechButton.innerHTML = '⏹️ Stop Recording';
                } else {
                    recognition.stop();
                    speechButton.innerHTML = '🎤 Voice Input';
                }
            };

            recognition.onresult = function(event) {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript;
                }
                answerTextarea.value = transcript;
                localStorage.setItem('interview_answer', transcript);
            };

            recognition.onend = function() {
                speechButton.innerHTML = '🎤 Voice Input';
            };
        }
    }
}

// Initialize speech recognition after DOM loads
document.addEventListener('DOMContentLoaded', startSpeechRecognition);