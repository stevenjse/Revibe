// Cargar historial de mensajes desde localStorage
const clearButton = document.getElementById('clear-chat');

function loadConversation() {
    const messages = JSON.parse(sessionStorage.getItem('chatHistory')) || [];
    messages.forEach(msg => appendMessage(msg.sender, msg.message, msg.button));
}

// Guardar el historial de mensajes en localStorage
function saveConversation(sender, message, button = null) {
    let chatHistory = JSON.parse(sessionStorage.getItem('chatHistory')) || [];
    chatHistory.push({ sender, message, button });
    sessionStorage.setItem('chatHistory', JSON.stringify(chatHistory));
}

// Borrar el historial de mensajes y actualizar la interfaz
function clearConversation() {
    sessionStorage.removeItem('chatHistory');
    conversation.innerHTML = '';
}

clearButton.addEventListener('click', function () {
    clearConversation();
});

messageForm.addEventListener('submit', function (event) {
    event.preventDefault();
    const message = messageInput.value;
    if (message.trim() !== '') {
        appendMessage('Tu', message);

        saveConversation('Tu', message);

        messageInput.value = '';
        sendMessageToServer(message);
    }
});

function appendMessage(sender, message, button = null) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;

    if (button) {
        const buttonElement = document.createElement('a');
        buttonElement.classList.add('btn', 'btn-primary');
        buttonElement.href = button.url;
        buttonElement.textContent = button.text;
        messageElement.appendChild(buttonElement);
    }

    conversation.appendChild(messageElement);
    conversation.scrollTop = conversation.scrollHeight;
}

function sendMessageToServer(message) {
    fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        if (data.response.button) {
            appendMessage('ChatBot', data.response.message, data.response.button);

            saveConversation('ChatBot', data.response.message, data.response.button);

        } else {
            appendMessage('ChatBot', data.response.message);

            saveConversation('ChatBot', data.response.message, data.response.button);

        }
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage('ChatBot', 'Lo siento, ha ocurrido un error.');
    });
}

// Cargar historial al iniciar
loadConversation();