document.addEventListener('DOMContentLoaded', () => {
    const inputField = document.getElementById('user-input');
    const sendButton = document.getElementById('send-btn');
    const chatBox = document.getElementById('chat-box');

    function appendMessage(isUser, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', isUser ? 'user-message' : 'bot-message');
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function sendMessageToServer(message) {
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'message': message })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage(false, data.reply);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    sendButton.addEventListener('click', () => {
        const message = inputField.value.trim();
        if (message) {
            appendMessage(true, message);
            sendMessageToServer(message);
            inputField.value = '';
        }
    });

    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const message = inputField.value.trim();
            if (message) {
                appendMessage(true, message);
                sendMessageToServer(message);
                inputField.value = '';
            }
        }
    });
});
