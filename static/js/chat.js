// Chat functionality for event livestreams

// Utility function to escape HTML to prevent XSS
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Create message element
function createMessageElement(message) {
    const isCurrentUser = message.username === currentUsername;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${isCurrentUser ? 'justify-end' : 'justify-start'} mb-3`;
    
    const messageBubble = document.createElement('div');
    messageBubble.className = isCurrentUser 
        ? 'bg-indigo-600 text-white rounded-lg py-2 px-4 max-w-xs'
        : 'bg-gray-200 text-gray-800 rounded-lg py-2 px-4 max-w-xs';
    
    const usernameEl = document.createElement('div');
    usernameEl.className = 'font-bold text-sm';
    usernameEl.textContent = isCurrentUser ? 'You' : escapeHtml(message.username);
    
    const messageTextEl = document.createElement('div');
    messageTextEl.textContent = escapeHtml(message.message);
    
    const timeEl = document.createElement('div');
    timeEl.className = 'text-xs opacity-75 text-right mt-1';
    timeEl.textContent = message.timestamp;
    
    messageBubble.appendChild(usernameEl);
    messageBubble.appendChild(messageTextEl);
    messageBubble.appendChild(timeEl);
    messageDiv.appendChild(messageBubble);
    
    return messageDiv;
}

// Global variables
let eventId;
let currentUsername;
let lastMessageId = 0;
let chatInterval;
let userCountInterval;
let randomUserCount;

// Initialize the chat functionality
function initChat(id, username) {
    eventId = id;
    currentUsername = username;
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message');
    
    if (!chatMessages || !chatForm || !messageInput) {
        console.error('Chat elements not found');
        return;
    }
    
    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!messageInput.value.trim()) {
            return;
        }
        
        // Get CSRF token from the form
        const csrfToken = document.querySelector('input[name="csrf_token"]').value;
        
        // Send the message to the server
        fetch(`/events/${eventId}/chat/send`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                message: messageInput.value,
                csrf_token: csrfToken
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Add the message to the chat
            const messageEl = createMessageElement(data);
            chatMessages.appendChild(messageEl);
            
            // Scroll to the bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Update the last message ID
            lastMessageId = data.id;
            
            // Clear the input field
            messageInput.value = '';
        })
        .catch(error => {
            console.error('Error sending message:', error);
        });
    });
    
    // For demo purposes, simulate some initial messages
    simulateInitialMessages();
    
    // Start polling for new messages
    fetchMessages();
    chatInterval = setInterval(fetchMessages, 3000);
    
    // Simulate changing user counts (for mock purposes)
    simulateUserCount();
    userCountInterval = setInterval(simulateUserCount, 10000);
    
    // Clean up when leaving the page
    window.addEventListener('beforeunload', function() {
        clearInterval(chatInterval);
        clearInterval(userCountInterval);
    });
}

// Fetch new messages
function fetchMessages() {
    fetch(`/events/${eventId}/chat/messages?last_id=${lastMessageId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(messages => {
            const chatMessages = document.getElementById('chat-messages');
            
            if (messages.length > 0) {
                messages.forEach(message => {
                    const messageEl = createMessageElement(message);
                    chatMessages.appendChild(messageEl);
                    lastMessageId = message.id;
                });
                
                // Scroll to the bottom if new messages arrived
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        })
        .catch(error => {
            console.error('Error fetching messages:', error);
        });
}

// Simulate initial messages for demo purposes
function simulateInitialMessages() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = ''; // Clear any placeholder
    
    const initialMessages = [
        {
            id: 1,
            username: 'EventHost',
            message: 'Welcome to the event! Feel free to ask questions in the chat.',
            timestamp: '12:00'
        },
        {
            id: 2,
            username: 'Attendee1',
            message: 'Looking forward to this session!',
            timestamp: '12:01'
        },
        {
            id: 3,
            username: 'Attendee2',
            message: 'Hello everyone! Joining from San Francisco.',
            timestamp: '12:02'
        }
    ];
    
    initialMessages.forEach(message => {
        const messageEl = createMessageElement(message);
        chatMessages.appendChild(messageEl);
    });
    
    // Set the last message ID to the highest ID in the simulated messages
    lastMessageId = Math.max(...initialMessages.map(m => m.id));
    
    // Scroll to the bottom initially
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Simulate changing user counts (for mock purposes)
function simulateUserCount() {
    const userCountElement = document.getElementById('user-count');
    if (userCountElement) {
        // Generate a random number between 10 and 100 if not already set
        if (!randomUserCount) {
            randomUserCount = Math.floor(Math.random() * 91) + 10;
        } else {
            // Randomly increase or decrease by 0-3
            const change = Math.floor(Math.random() * 7) - 3;
            randomUserCount = Math.max(5, randomUserCount + change);
        }
        
        userCountElement.textContent = randomUserCount;
    }
}
