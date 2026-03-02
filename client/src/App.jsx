import React, { useEffect, useRef, useState } from 'react';
import { useChat } from './hooks/useChat';
import MessageItem from './components/MessageItem';
import AdminPanel from './components/AdminPanel';
import RecommendedVideos from './components/RecommendedVideos';
import streamThumb from './assets/stream_thumb.jpg';
import './App.css'; // We'll move the CSS here

function App() {
  const { messages, inputText, setInputText, sendMessage, clearChat, handleTyping, typingUsers } = useChat();
  const chatEndRef = useRef(null);
  // State for floating reactions
  const [floatingReactions, setFloatingReactions] = useState([]);
  // State for chat visibility
  const [isChatOpen, setIsChatOpen] = useState(true);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (isChatOpen) {
      scrollToBottom();
    }
  }, [messages, isChatOpen, typingUsers]); // Scroll when typing users change too

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  const handleInputChange = (e) => {
    setInputText(e.target.value);
    handleTyping();
  };

  const addReaction = (emoji) => {
    // 1. DO NOT Add to input (User requested change)
    // setInputText(prev => prev + emoji);

    // 2. Add 5 floating reactions per click (Burst effect)
    const newReactions = [];
    for (let i = 0; i < 5; i++) {
      const id = Date.now() + Math.random();
      // Random position between 20% and 80% of the container width to keep them centralized but spread
      const randomLeft = Math.floor(Math.random() * 60) + 20;
      const randomDelay = Math.random() * 0.5; // Random delay between 0 and 0.5s for burst feel

      newReactions.push({ id, emoji, left: randomLeft, delay: randomDelay });
    }

    setFloatingReactions(prev => [...prev, ...newReactions]);

    // 3. Remove after 3 seconds (2s animation + max 0.5s delay + buffer)
    setTimeout(() => {
      const idsToRemove = newReactions.map(r => r.id);
      setFloatingReactions(prev => prev.filter(r => !idsToRemove.includes(r.id)));
    }, 3000);
  };

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const [isAdminOpen, setIsAdminOpen] = useState(false);

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-left">
          <button className="menu-btn">☰</button>
          <div className="logo">
            <span className="logo-icon">▶</span>
            <span className="logo-text">YouTube</span>
          </div>
        </div>
        <div className="header-center">
          <div className="search-bar">
            <input type="text" placeholder="Search" />
            <button className="search-btn">🔍</button>
          </div>
          <button className="voice-search-btn">🎤</button>
        </div>
        <div className="header-right">
          <button className="icon-btn">📹</button>
          <button className="icon-btn">🔔</button>
          <div className="profile-icon">Y</div>
        </div>
      </header>

      <div className="content-wrapper">
        {/* main-content: Video + Details */}
        <div className="main-content">
          <div className="video-player-section">
            <div className="video-wrapper">
              {/* Stream Thumbnail */}
              <img
                src={streamThumb}
                alt="Cyberpunk 2077 Stream"
                className="video-thumbnail"
              />
              <div className="live-badge-overlay">🔴 LIVE</div>
              <div className="view-count-overlay">👁 15K</div>
            </div>
          </div>

          {/* Video Info & Actions */}
          <div className="video-info-section">
            <h1 className="video-title">Cyberpunk 2077 - Night City Walkthrough [4K 60FPS]</h1>

            <div className="video-meta-row">
              <div className="channel-info">
                <div className="channel-avatar">G</div>
                <div className="channel-text">
                  <h3>Gaming</h3>
                  <p>1.2M subscribers</p>
                </div>
                <button className="subscribe-btn">Subscribe</button>
              </div>

              <div className="actions-buttons">
                <div className="like-dislike-group">
                  <button className="action-btn like-btn" title="I like this">
                    👍 12K
                  </button>
                  <div className="separator-vertical"></div>
                  <button className="action-btn dislike-btn" title="I dislike this">
                    👎
                  </button>
                </div>

                <button
                  className="action-btn share-btn"
                  onClick={() => {
                    const url = window.location.origin;
                    navigator.clipboard.writeText(url).then(() => {
                      alert(`Link copied! Configure your firewall if needed.\nShare this link: ${url}`);
                    }).catch(console.error);
                  }}
                >
                  ↗️ Share
                </button>

                <button className="action-btn download-btn">
                  ⬇️ Download
                </button>

                <button className="action-btn ellipses-btn">...</button>
              </div>
            </div>

            <div className="description-box">
              <p className="views-date">94,321 views • Streamed live 2 hours ago</p>
              <p>Exploring the neon-lit streets of Night City. Testing the new AI-powered toxicity detection system in the chat!</p>
              <button className="show-more-btn">Show more</button>
            </div>

            <div className="comments-section-placeholder">
              <h3>Comments turned off for this stream. join live chat!</h3>
            </div>

            {/* Recommended Videos (Sidebar style, but placed here for responsive layout) */}
            <RecommendedVideos />
          </div>
        </div>

        {/* Side Panel (Chat + Recommendations) */}
        <div className="side-panel">
          {isChatOpen && (
            <div className="chat-container">
              <div className="chat-header">
                <div className="header-content">
                  <span>Top chat</span>
                  <span className="dropdown-arrow">▼</span>
                </div>
                <div className="header-actions">
                  <button className="header-icon-btn">⋮</button>
                  <button className="clear-btn" onClick={clearChat} title="Clear Chat History">
                    ❌
                  </button>
                </div>
              </div>

              <div className="chat-messages">
                <div className="pinned-message">
                  <div className="pin-icon">📌</div>
                  <div className="pin-content">
                    <span className="pin-author">Moderator</span>
                    <span className="pin-text">Welcome to the stream! Please be respectful.</span>
                  </div>
                </div>

                {messages.map((msg) => (
                  <MessageItem key={msg.id} message={msg} />
                ))}

                {/* Typing Indicator */}
                {typingUsers.size > 0 && (
                  <div className="typing-indicator" style={{ padding: '8px', fontSize: '0.8rem', color: '#aaa', fontStyle: 'italic' }}>
                    {Array.from(typingUsers).join(', ')} is typing...
                  </div>
                )}

                <div ref={chatEndRef} />

              </div>

              <div className="chat-footer">
                <div className="chat-input-area">
                  <div className="input-wrapper">
                    <div className="user-avatar-small">Y</div>
                    <div className="input-box-wrapper">
                      <span className="placeholder-text" style={{ display: inputText ? 'none' : 'block' }}>Chat...</span>
                      <input
                        type="text"
                        id="message-input"
                        maxLength="200"
                        autoComplete="off"
                        value={inputText}
                        onChange={handleInputChange}
                        onKeyPress={handleKeyPress}
                      />
                      <div className="input-actions-floating">
                        <button className="emoji-btn">😊</button>
                        <span className="char-count">{inputText.length}/200</span>
                      </div>
                    </div>
                    <button
                      id="send-btn"
                      onClick={sendMessage}
                      disabled={!inputText.trim()}
                    >
                      <svg viewBox="0 0 24 24" preserveAspectRatio="xMidYMid meet" focusable="false" style={{ pointerEvents: 'none', display: 'block', width: '24px', height: '24px' }}><g className="style-scope yt-icon"><path d="M2,21L23,12L2,3V10L17,12L2,14V21Z" className="style-scope yt-icon"></path></g></svg>
                    </button>
                  </div>
                </div>

                {/* Reaction Buttons Row - Moved to bottom like typical live interactions */}
                <div className="reaction-bar">
                  <div className="reaction-emojis">
                    <button onClick={() => addReaction('🔥')}>🔥</button>
                    <button onClick={() => addReaction('❤️')}>❤️</button>
                    <button onClick={() => addReaction('😂')}>😂</button>
                    <button onClick={() => addReaction('👍')}>👍</button>
                    <button onClick={() => addReaction('💯')}>💯</button>
                  </div>
                  <div className="chat-visibility-toggle">
                    <button className="hide-chat-text-btn" onClick={toggleChat}>Hide chat</button>
                  </div>
                </div>
              </div>

              {/* Floating Reactions Overlay (Moved to chat container level) */}
              <div className="floating-reactions-container">
                {floatingReactions.map(reaction => (
                  <div
                    key={reaction.id}
                    className="floating-emoji"
                    style={{
                      left: `${reaction.left}%`,
                      animationDelay: `${reaction.delay}s`
                    }}
                  >
                    {reaction.emoji}
                  </div>
                ))}
              </div>

            </div>
          )}

          {/* Recommended Videos (Removed) */}
          {/* <RecommendedVideos /> */}
        </div>
      </div>

      {/* Floating Buttons on bottom right if chat is closed */}
      {
        !isChatOpen && (
          <button className="floating-chat-btn" onClick={toggleChat}>
            Show Chat
          </button>
        )
      }

      {/* Admin Button - Floating */}
      <button className="floating-admin-btn" onClick={() => setIsAdminOpen(!isAdminOpen)}>
        ⚙️
      </button>
      {
        isAdminOpen && (
          <AdminPanel onClose={() => setIsAdminOpen(false)} />
        )
      }
    </div >
  );
}

export default App;
