document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const charCount = document.getElementById('char-count');
    
    // Initial sync
    fetchMessages();
    
    // Poll for messages every 1 second (simulating real-time)
    setInterval(fetchMessages, 1000);

    // Input handling
    messageInput.addEventListener('input', () => {
        const length = messageInput.value.length;
        charCount.textContent = `${length}/200`;
        sendBtn.disabled = length === 0;
    });

    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !sendBtn.disabled) {
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', () => {
        if (!sendBtn.disabled) {
            sendMessage();
        }
    });

    function sendMessage() {
        const text = messageInput.value.trim();
        if (!text) return;

        // Clear input immediately for better UX
        messageInput.value = '';
        charCount.textContent = '0/200';
        sendBtn.disabled = true;

        // POST to backend
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: text,
                username: 'You' // In a real app this would be the logged-in user
            })
        })
        .then(response => response.json())
        .then(data => {
            // Check urgency action
            if (data.action === 'warn') {
                // Determine if this is a "toxic" message that needs the user warning ALERT
                alert("You should not use these words or you are using toxic words on live chat.");
            }
            // We append the message manually here for instant feedback OR wait for poll?
            // "No lag in message appearance." -> Append manually if it's my message.
            renderMessage(data, true); // true = append to bottom
        })
        .catch(err => console.error('Error sending message:', err));
    }

    let displayedMessageIds = new Set();

    function fetchMessages() {
        fetch('/messages')
        .then(response => response.json())
        .then(messages => {
            // Filter out messages we already displayed
            // However, we need to be careful not to duplicate if we manually gathered it.
            // For simplicity in this demo: we could just redraw or only append new ones.
            // Let's only append new ones based on ID.
            
            messages.forEach(msg => {
                if (!displayedMessageIds.has(msg.id)) {
                    renderMessage(msg);
                }
            });
        });
    }

    function renderMessage(msg, scroll = true) {
        if (displayedMessageIds.has(msg.id)) return;
        displayedMessageIds.add(msg.id);

        const msgDiv = document.createElement('div');
        msgDiv.className = 'message-item';
        msgDiv.dataset.id = msg.id;

        // Generate a random color for the avatar if generic
        const avatarColor = stringToColor(msg.username);
        const avatarLetter = msg.username.charAt(0).toUpperCase();

        let innerHTML = `
            <div class="avatar" style="background-color: ${avatarColor}">${avatarLetter}</div>
            <div class="message-content">
                <span class="author-name">${escapeHtml(msg.username)}</span>
        `;

        if (msg.type === 'toxic') {
            msgDiv.classList.add('toxic-system-msg');
            innerHTML += `<span class="message-text">${escapeHtml(msg.display_text)}</span>`;
            
            // Auto schedule removal
            setTimeout(() => {
                removeMessage(msgDiv);
            }, 7000); // 7 seconds
        } else {
            innerHTML += `<span class="message-text">${escapeHtml(msg.display_text)}</span>`;
        }

        innerHTML += `</div>`;
        msgDiv.innerHTML = innerHTML;

        chatMessages.appendChild(msgDiv);

        if (scroll) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    function removeMessage(element) {
        // Smooth fade out
        element.style.animation = 'fadeOut 0.5s ease-out forwards';
        setTimeout(() => {
            element.remove();
        }, 500);
    }

    // Utility to generate consistent colors from names
    function stringToColor(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        const c = (hash & 0x00FFFFFF).toString(16).toUpperCase();
        return '#' + '00000'.substring(0, 6 - c.length) + c;
    }

    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }
});
