// Django Dashboard JavaScript for AI interactions

let currentCredits = parseInt(document.getElementById('nav-credits')?.textContent) || 0;

// AI Tutor Chat
document.getElementById('tutor-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const questionInput = document.getElementById('question-input');
    const askBtn = document.getElementById('ask-btn');
    const question = questionInput.value.trim();
    
    if (!question) {
        showToast('Please enter a question', 'warning');
        return;
    }
    
    if (currentCredits < 1) {
        showToast('Insufficient credits. Please purchase more.', 'danger');
        return;
    }
    
    // Show user message
    addChatMessage(question, 'user');
    
    // Clear input and show loading
    questionInput.value = '';
    const originalContent = showLoading(askBtn, 'Thinking...');
    
    // Send to AI
    fetch('/ai/tutor/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading(askBtn, originalContent);
        
        if (data.error) {
            showToast(data.error, 'danger');
            return;
        }
        
        // Show AI response
        addChatMessage(data.response, 'ai');
        
        // Update credits
        currentCredits = data.credits_remaining;
        updateCreditsDisplay(currentCredits);
        
        showToast('Response generated successfully!', 'success');
    })
    .catch(error => {
        hideLoading(askBtn, originalContent);
        handleAPIError(error, 'Failed to get AI response');
    });
});

function addChatMessage(message, sender) {
    const chatContainer = document.getElementById('chat-container');
    
    // Remove welcome message if it exists
    const welcomeMessage = chatContainer.querySelector('.text-center.text-muted');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender === 'user' ? 'user-message' : 'ai-response'}`;
    
    const senderLabel = sender === 'user' ? 'You' : 'AI Tutor';
    const icon = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
    
    messageDiv.innerHTML = `
        <div class="d-flex align-items-start">
            <i class="${icon} me-2 mt-1"></i>
            <div>
                <strong>${senderLabel}:</strong>
                <div class="mt-1">${formatMessage(message)}</div>
            </div>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function formatMessage(message) {
    // Basic formatting for AI responses
    return message
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^(.*)$/, '<p>$1</p>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');
}

// Explain Concept Modal
function showExplainModal() {
    const modal = new bootstrap.Modal(document.getElementById('explainModal'));
    modal.show();
}

document.getElementById('explain-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (currentCredits < 2) {
        showToast('Insufficient credits (2 required)', 'danger');
        return;
    }
    
    const topic = document.getElementById('topic').value.trim();
    const level = document.getElementById('level').value;
    const context = document.getElementById('context').value.trim();
    
    if (!topic) {
        showToast('Please enter a topic', 'warning');
        return;
    }
    
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalContent = showLoading(submitBtn, 'Generating...');
    
    fetch('/ai/explain/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            topic: topic,
            level: level,
            context: context
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading(submitBtn, originalContent);
        
        if (data.error) {
            showToast(data.error, 'danger');
            return;
        }
        
        // Add explanation to chat
        addChatMessage(`Explain: ${topic} (${level} level)`, 'user');
        addChatMessage(data.explanation, 'ai');
        
        // Update credits
        currentCredits = data.credits_remaining;
        updateCreditsDisplay(currentCredits);
        
        // Close modal and reset form
        bootstrap.Modal.getInstance(document.getElementById('explainModal')).hide();
        this.reset();
        
        showToast('Explanation generated successfully!', 'success');
    })
    .catch(error => {
        hideLoading(submitBtn, originalContent);
        handleAPIError(error, 'Failed to generate explanation');
    });
});

// Quiz Generator Modal
function showQuizModal() {
    const modal = new bootstrap.Modal(document.getElementById('quizModal'));
    modal.show();
}

document.getElementById('quiz-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (currentCredits < 3) {
        showToast('Insufficient credits (3 required)', 'danger');
        return;
    }
    
    const topic = document.getElementById('quiz-topic').value.trim();
    const difficulty = document.getElementById('difficulty').value;
    const numQuestions = document.getElementById('num-questions').value;
    
    if (!topic) {
        showToast('Please enter a quiz topic', 'warning');
        return;
    }
    
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalContent = showLoading(submitBtn, 'Creating Quiz...');
    
    fetch('/ai/generate-quiz/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            topic: topic,
            difficulty: difficulty,
            num_questions: parseInt(numQuestions)
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading(submitBtn, originalContent);
        
        if (data.error) {
            showToast(data.error, 'danger');
            return;
        }
        
        // Add quiz to chat
        addChatMessage(`Generate ${difficulty} quiz: ${topic} (${numQuestions} questions)`, 'user');
        addChatMessage(data.quiz_content, 'ai');
        
        // Update credits
        currentCredits = data.credits_remaining;
        updateCreditsDisplay(currentCredits);
        
        // Close modal and reset form
        bootstrap.Modal.getInstance(document.getElementById('quizModal')).hide();
        this.reset();
        
        showToast('Quiz generated successfully!', 'success');
    })
    .catch(error => {
        hideLoading(submitBtn, originalContent);
        handleAPIError(error, 'Failed to generate quiz');
    });
});

// IntaSend Payment Integration for Django
function purchaseCredits(credits, price) {
    // Create checkout session
    fetch('/payments/create-checkout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ credits: credits })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }
        
        // Initialize IntaSend checkout
        const checkout = new IntaSendCheckout(data.checkout_data);
        checkout.popup();
        
        checkout.on('completed', function(result) {
            alert('Payment successful! Credits will be added shortly.');
            window.location.reload();
        });
        
        checkout.on('failed', function(result) {
            alert('Payment failed. Please try again.');
        });
    })
    .catch(error => {
        console.error('Checkout error:', error);
        alert('Failed to create checkout session');
    });
}

