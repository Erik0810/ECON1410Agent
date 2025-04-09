document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const newChatButton = document.getElementById('new-chat-button');
    const chatMessages = document.getElementById('chat-messages');
    let currentSpacer = null;

    // Sending messages
    const sendMessage = async () => {
        const message = messageInput.value.trim();
        if (!message) return;

        // Remove previous spacer if it exists
        if (currentSpacer) {
            currentSpacer.remove();
            currentSpacer = null;
        }

        // Display user message
        const userMessageHeight = appendMessage(message, 'user');

        // Add spacer for expected AI response
        const spacer = document.createElement('div');
        spacer.className = 'response-spacer';
        spacer.style.height = '60vh';
        chatMessages.appendChild(spacer);
        currentSpacer = spacer;

        // Scroll to position user message at top
        const container = chatMessages.parentElement;
        container.scrollTop = chatMessages.scrollHeight - container.clientHeight;

        messageInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            // Add AI response but keep the spacer
            appendMessage(data.response, 'ai');
        } catch (error) {
            appendMessage('Sorry, there was an error processing your request.', 'ai');
            console.error('Error:', error);
        }
    };

    // Create and append message to chat
    const appendMessage = (text, sender) => {
        const wrapper = document.createElement('div');
        wrapper.className = `message-wrapper ${sender}-wrapper`;

        // Profile icon
        const profileIcon = document.createElement('div');
        profileIcon.className = `profile-icon ${sender}-icon`;
        profileIcon.innerHTML = sender === 'user' ? 
            '<i class="bi bi-person-circle"></i>' : 
            '<i class="bi bi-robot"></i>';

        // Create message div
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        // Format AI messages with proper spacing and formatting
        if (sender === 'ai') {
            // Convert markdown-style code blocks to HTML
            text = text.replace(/```(\w*)\n([\s\S]*?)```/g, 
                (match, language, code) => `<pre><code>${code.trim()}</code></pre>`);
            
            // Convert bullet points
            text = text.replace(/^\s*[-*]\s(.+)$/gm, '<li>$1</li>');
            if (text.includes('<li>')) {
                text = '<ul>' + text + '</ul>';
            }
            
            // Handle bold and italic text
            text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
            
            // Convert line breaks to paragraphs
            text = text.split('\n\n').map(p => `<p>${p.trim()}</p>`).join('');
        }
        
        messageDiv.innerHTML = text;

        // Assemble the message wrapper
        wrapper.appendChild(profileIcon);
        wrapper.appendChild(messageDiv);

        // Insert before the spacer if it exists
        if (currentSpacer) {
            chatMessages.insertBefore(wrapper, currentSpacer);
        } else {
            chatMessages.appendChild(wrapper);
        }

        return wrapper.offsetHeight;
    };

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Mobile touch event for send button
    sendButton.addEventListener('touchend', (e) => {
        e.preventDefault();
        sendMessage();
    });

    // Start new chat functionality
    // Make this clear pending messages from the ai in the future
    newChatButton.addEventListener('click', () => {
        chatMessages.innerHTML = '';
        messageInput.value = '';
        currentSpacer = null;
    });

    // Loading indicator
    // Not implemented fully yet
    const setLoading = (isLoading) => {
        sendButton.disabled = isLoading;
        messageInput.disabled = isLoading;
        sendButton.innerHTML = isLoading ? 
            '<span class="spinner-border spinner-border-sm"></span>' : 
            'Send';
    };
});