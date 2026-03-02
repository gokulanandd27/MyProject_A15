import React, { useEffect, useState } from 'react';

const stringToColor = (str) => {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    const c = (hash & 0x00FFFFFF).toString(16).toUpperCase();
    return '#' + '00000'.substring(0, 6 - c.length) + c;
};

const MessageItem = ({ message }) => {
    // Initialize with original text
    const [displayText, setDisplayText] = useState(message.display_text);
    const [isRemoved, setIsRemoved] = useState(false);

    useEffect(() => {
        // Check if message is toxic
        const isToxicContent = message.type === 'toxic' || message.is_toxic;

        if (isToxicContent) {
            // Calculate remaining time for 7-second window
            // message.id is assumed to be timestamp in ms
            const createdTime = message.id;
            const now = Date.now();
            const elapsed = now - createdTime;
            const targetDuration = 7000; // 7 seconds
            const remaining = targetDuration - elapsed;

            const hideMessage = () => {
                const severity = message.severity || "Toxic";
                const reason = message.reason || "Violates community guidelines";
                setDisplayText(`${severity} Severity - ${reason}`);
                setIsRemoved(true);
            };

            if (remaining <= 0) {
                // Time already passed, hide immediately
                hideMessage();
            } else {
                // Wait for remaining time
                const timer = setTimeout(() => {
                    hideMessage();
                }, remaining);
                return () => clearTimeout(timer);
            }
        }
    }, [message]);

    const isToxic = message.type === 'toxic' || message.is_toxic;
    const avatarLetter = (message.username || "U").charAt(0).toUpperCase();
    const avatarColor = stringToColor(message.username || "User");

    // Dynamic class based on severity
    let severityClass = '';
    if (isToxic) {
        const sev = (message.severity || 'High').toLowerCase(); // high, medium, low
        severityClass = `toxic-${sev}`;
    }

    // Apply severity style immediately if toxic
    // Apply toxic-system-msg style ONLY when removed (isRemoved is true)
    const isSystem = message.type === 'system';
    const messageClass = `message-item ${isToxic ? severityClass : ''} ${isRemoved ? 'toxic-system-msg' : ''} ${isSystem ? 'system-msg' : ''}`;

    return (
        <div className={messageClass}>
            <div className="avatar" style={{ backgroundColor: avatarColor }}>
                {avatarLetter}
            </div>
            <div className="message-content">
                <span className="author-name">{message.username}</span>
                <span className="message-text">
                    {/* Show [REMOVED] tag only when actually removed */}
                    {isRemoved && <strong>[REMOVED] </strong>}
                    {displayText}
                </span>
            </div>
        </div>
    );
};

export default MessageItem;
