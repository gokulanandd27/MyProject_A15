import { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const useChat = () => {
  const [serverMessages, setServerMessages] = useState([]);
  const [localMessages, setLocalMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [typingUsers, setTypingUsers] = useState(new Set()); // Kept empty or dummy if we remove socket
  const displayedMessageIds = useRef(new Set());
  const intervalRef = useRef(null);

  // Poll for messages
  useEffect(() => {
    fetchMessages();
    intervalRef.current = setInterval(fetchMessages, 1000); // Poll every second

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await axios.get(`${API_URL}/messages`);
      // Basic dedup logic if needed, or just set
      // setMessages(response.data);
      // To mimic the stream behavior, we might want to append new ones only?
      // But get_messages returns full list.
      // Let's just set it for robustness in polling
      setServerMessages(response.data);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  // Random data for bots
  const botNames = [
    "ViperStack", "ShadowMonk", "Luna_Plays", "IronFist_99", "NeonDrifter", 
    "GokulFan_007", "TamilGamer_YT", "Chennai_Express", "Rogue_Agent", "Pixel_Master",
    "SniperWolf_Xx", "TechGeek_123", "Mystic_Aura", "StormBreaker", "Night_Owl",
    "Pro_Gamer_Ind", "Cyber_Samurai", "Vel_Gaming", "Thala_Fan", "Gaming_Queen"
  ];
  
  const botMessages = [
    "This game is insane!", "OMG did you see that?", "LOL", "Can you play Minecraft next?", 
    "Nice moves!", "What specs do you have?", "Hello from India!", "Big fan!", 
    "Is this 4K?", "Lag?", "Op gameplay", "GG", "Next level skills", 
    "When is the giveaway?", "First time here, amazing content!",
    "Bro which sensitivity settings are you using right now?",
    "Can you clutch this round without using any special skills?",
    "Which map do you enjoy playing the most and why?",
    "Is this your main account or just a secondary one?",
    "How do you stay calm during intense clutch moments?",
    "Can you try a risky move just for chat?",
    "What rank are you aiming for by season end?",
    "Do you play better solo or with full squad?",
    "Which headset or gear are you currently using?",
    "Any beginner tips for players watching this stream live?"
  ];

  const triggerBotMessages = async () => {
    // Send 5 random messages
    for (let i = 0; i < 5; i++) {
        const delay = Math.floor(Math.random() * 1500) + 500;
        await new Promise(resolve => setTimeout(resolve, delay));
        
        const randomName = botNames[Math.floor(Math.random() * botNames.length)];
        const randomMsg = botMessages[Math.floor(Math.random() * botMessages.length)];
        
        // Post bot message to API? 
        // Or just add to local state? 
        // Adding to API is better so they persist in "poll"
        try {
            await axios.post(`${API_URL}/analyze`, {
                message: randomMsg,
                username: randomName
            });
            // Polling will pick it up
        } catch (e) {
            console.error(e);
        }
    }
  };

  const sendMessage = async () => {
    if (!inputText.trim()) return;

    try {
        const payload = {
            message: inputText,
            username: 'You' 
        };
        const response = await axios.post(`${API_URL}/analyze`, payload);
        
        if (response.data.id && response.data.username === 'System') {
              // Warning message (Any system message) - keep for 15s
              setLocalMessages(prev => [...prev, response.data]);
              setTimeout(() => {
                  setLocalMessages(prev => prev.filter(m => m.id !== response.data.id));
              }, 15000); 
        } else {
             // Normal message, optimistic update
             setServerMessages(prev => [...prev, response.data]);
        }
        
        setInputText('');

        // Trigger bots
        triggerBotMessages();
    } catch (error) {
        console.error("Error sending message:", error);
    }
  };

  const handleTyping = () => {
    // No-op in polling mode usually, unless we have an endpoint
  };

  const clearChat = async () => {
    try {
      await axios.post(`${API_URL}/clear_chat`);
      setServerMessages([]);
      setLocalMessages([]);
    } catch (error) {
      console.error("Error clearing chat:", error);
    }
  };

  // We can keep hideMessage locally if user wants that feature "old" project might not have had it.
  // But user said "reverse to old", so I will remove it to be safe.
  
  // Combine messages to return
  const messages = [...serverMessages, ...localMessages].sort((a, b) => a.id - b.id);
  
  return {
    messages,
    inputText,
    setInputText,
    sendMessage,
    clearChat,
    handleTyping,
    typingUsers // will be empty
  };
};
