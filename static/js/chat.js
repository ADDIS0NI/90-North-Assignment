// static/js/chat.js
class ChatManager {
    constructor() {
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.messageInput = document.querySelector('#chat-message-input');
        this.submitButton = document.querySelector('#chat-message-submit');
        this.statusElement = document.getElementById('connection-status');
        this.messagesContainer = document.querySelector('#chat-messages');

        this.initializeEventListeners();
        this.connectWebSocket();
    }

    connectWebSocket() {
        console.log("Attempting to connect to WebSocket...");
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/chat/`;
        console.log(`Connecting to WebSocket at: ${wsUrl}`);
        
        this.socket = new WebSocket(wsUrl);
    
        this.socket.onopen = () => {
            console.log("WebSocket connection established!");
            this.handleOpen();
        };
    
        this.socket.onerror = (error) => {
            console.error("WebSocket error:", error);
            this.handleError(error);
        };
    
        this.socket.onclose = (event) => {
            console.log("WebSocket closed:", event);
            this.handleClose(event);
        };
    
        this.socket.onmessage = (event) => {
            console.log("WebSocket message received");
            this.handleMessage(event);
        };
    }

    handleOpen() {
        console.log("WebSocket connection established!");
        this.updateStatus('Connected', 'green');
    }

    handleMessage(event) {
        const data = JSON.parse(event.data);
        const messageElement = document.createElement('div');
        const currentUserEmail = document.querySelector('.chat-container').dataset.userEmail;
        
        // Create message container
        messageElement.className = `message ${data.user_email === currentUserEmail ? 'sent' : 'received'}`;
        
        // Create message content
        const messageHTML = `
            <div class="message-header">${data.user_email === currentUserEmail ? 'You' : data.user_email}</div>
            <div class="message-text">${data.message}</div>
        `;
        messageElement.innerHTML = messageHTML;
        
        this.messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    handleClose(event) {
        console.log("WebSocket connection closed", event);
        this.updateStatus('Disconnected', 'red');

        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            setTimeout(() => this.connectWebSocket(), 3000);
        }
    }

    handleError(error) {
        console.error("WebSocket error:", error);
    }

    updateStatus(message, color) {
        this.statusElement.textContent = message;
        this.statusElement.style.color = color;
    }

    initializeEventListeners() {
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        this.submitButton.addEventListener('click', () => this.sendMessage());
    }

    sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (message && this.socket?.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({ 'message': message }));
            this.messageInput.value = '';
        }
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.chat-container')) {
        new ChatManager();
    }
});