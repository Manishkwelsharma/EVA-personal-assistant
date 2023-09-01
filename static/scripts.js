document.addEventListener('DOMContentLoaded', () => {
    const chatDiv = document.getElementById('chat');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');

    sendBtn.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message !== '') {
            displayMessage('user', message);
            sendUserMessage(message);
            userInput.value = '';
        }
    });

    function displayMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = text;
        chatDiv.appendChild(messageDiv);
        chatDiv.scrollTop = chatDiv.scrollHeight;
    }

    function sendUserMessage(message) {
        fetch('/get_response', {
            method: 'POST',
            body: new URLSearchParams({
                user_input: message
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.text())
        .then(data => {
            displayMessage('chatbot', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
