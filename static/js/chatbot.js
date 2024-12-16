const chatButton = document.getElementById('chat-button');
const chatContainer = document.getElementById('chat-container');

const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');
const conversation = document.getElementById('conversation');
const closeButton = document.getElementById('close-chat');


// Cargar historial de mensajes desde localStorage
function loadConversation() {
    const messages = JSON.parse(localStorage.getItem('chatHistory')) || [];
    messages.forEach(msg => appendMessage(msg.sender, msg.message, msg.button));
}

// Guardar el historial de mensajes en localStorage
function saveConversation(sender, message, button = null) {
    let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
    chatHistory.push({ sender, message, button });
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
}


closeButton.addEventListener('click', function () {
    chatContainer.style.display = 'none';
    chatButton.style.display = 'block';
});

let chatOpen = false;

chatButton.addEventListener('click', function () {
    chatContainer.style.display = 'block';
    chatButton.style.display = 'none';
    chatOpen = true;

    if (conversation.children.length === 0) {
        appendMessage('ChatBot', 'Hola, ¿Cuáles opciones necesitas?\n1. Cómo vender\n2. Cómo comprar\n3. Devoluciones\n4. Otros');
        saveConversation('ChatBot', 'Hola, ¿Cuáles opciones necesitas?\n1. Cómo vender\n2. Cómo comprar\n3. Devoluciones\n4. Otros');
    }

});

// closeButton.addEventListener('click', function () {
//     chatContainer.style.display = 'none';
//     chatButton.style.display = 'block';
//     chatOpen = false;
// });

// messageForm.addEventListener('submit', function (event) {
//     event.preventDefault();
//     const message = messageInput.value;
//     if (message.trim() !== '') {
//         appendMessage('Tu', message);
//         messageInput.value = '';
//     }
// });

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