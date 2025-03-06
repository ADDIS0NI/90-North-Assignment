// Common functionality and utilities
class Utils {
    static showMessage(message, type = 'info') {
        const messageContainer = document.createElement('div');
        messageContainer.className = `alert alert-${type}`;
        messageContainer.textContent = message;
        
        const messagesDiv = document.querySelector('.messages');
        if (messagesDiv) {
            messagesDiv.appendChild(messageContainer);
            setTimeout(() => messageContainer.remove(), 5000);
        }
    }
}

// Global error handling
window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
    Utils.showMessage('An error occurred. Please try again.', 'error');
});

// Auto-dismiss alerts
// Auto-dismiss alerts (excluding chat)
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert:not(.chat-message)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease-in-out forwards';
            setTimeout(() => alert.remove(), 300);
        }, 3000);
    });
});