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
        
        // Get the correct WebSocket URL
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/chat/`;
        
        console.log(`Connecting to WebSocket at: ${wsUrl}`);
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = () => this.handleOpen();
        this.socket.onmessage = (e) => this.handleMessage(e);
        this.socket.onclose = (e) => this.handleClose(e);
        this.socket.onerror = (e) => this.handleError(e);
    }

    handleOpen() {
        console.log("WebSocket connection established!");
        this.updateStatus('Connected', 'green');
        this.reconnectAttempts = 0; // Reset reconnect attempts on successful connection
    }

    handleMessage(event) {
        console.log("Message received:", event.data);
        try {
            const data = JSON.parse(event.data);
            
            // Check if there's an error message
            if (data.error) {
                console.error("Error from server:", data.error);
                return;
            }
            
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
        } catch (error) {
            console.error("Error parsing message:", error);
        }
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    handleClose(event) {
        console.log("WebSocket connection closed", event);
        this.updateStatus('Disconnected', 'red');

        // Attempt to reconnect with exponential backoff
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(3000 * Math.pow(1.5, this.reconnectAttempts - 1), 30000);
            console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            
            this.updateStatus(`Reconnecting in ${Math.round(delay/1000)}s...`, 'orange');
            setTimeout(() => this.connectWebSocket(), delay);
        } else {
            this.updateStatus('Connection failed. Please refresh the page.', 'red');
        }
    }

    handleError(error) {
        console.error("WebSocket error:", error);
        this.updateStatus('Connection error', 'red');
    }

    updateStatus(message, color) {
        if (this.statusElement) {
            this.statusElement.textContent = message;
            this.statusElement.style.color = color;
        }
    }

    initializeEventListeners() {
        if (this.messageInput) {
            this.messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }

        if (this.submitButton) {
            this.submitButton.addEventListener('click', () => this.sendMessage());
        }
    }

    sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (message && this.socket?.readyState === WebSocket.OPEN) {
            console.log("Sending message:", message);
            this.socket.send(JSON.stringify({ 'message': message }));
            this.messageInput.value = '';
        } else if (this.socket?.readyState !== WebSocket.OPEN) {
            console.warn("Cannot send message: WebSocket is not open");
            this.updateStatus('Not connected. Message not sent.', 'red');
            setTimeout(() => this.updateStatus('Disconnected', 'red'), 3000);
        }
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM loaded, checking for chat container");
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        console.log("Chat container found, initializing ChatManager");
        new ChatManager();
    } else {
        console.log("No chat container found on this page");
    }
});