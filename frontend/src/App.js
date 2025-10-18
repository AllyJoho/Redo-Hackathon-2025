import React, { useState, useEffect, useRef } from 'react';
import './styles/App.css';
import ChatMessage from './components/ChatMessage';
import MajorCard from './components/MajorCard';
import ScheduleDisplay from './components/ScheduleDisplay';
import { sendChatMessage, generateSchedule } from './services/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [recommendedMajors, setRecommendedMajors] = useState([]);
  const [majorDetails, setMajorDetails] = useState([]);
  const [schedule, setSchedule] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (messageText = null) => {
    const textToSend = messageText || inputMessage;
    
    if (!textToSend.trim()) return;

    // Add user message to chat
    const newMessages = [...messages, { role: 'user', content: textToSend }];
    setMessages(newMessages);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Send to API
      const response = await sendChatMessage(textToSend);
      const data = response.data;

      // Add AI response to chat
      setMessages([...newMessages, { role: 'assistant', content: data.response }]);

      // Update recommended majors if provided
      if (data.recommended_majors && data.recommended_majors.length > 0) {
        setRecommendedMajors(data.recommended_majors);
        setMajorDetails(data.major_details || []);
      }

    } catch (error) {
      console.error('Error sending message:', error);
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateSchedule = async () => {
    if (recommendedMajors.length === 0) {
      setMessages([
        ...messages,
        {
          role: 'assistant',
          content: 'Please tell me about your interests first so I can recommend majors!',
        },
      ]);
      return;
    }

    setIsLoading(true);

    try {
      const response = await generateSchedule(recommendedMajors);
      const data = response.data;

      if (data.success) {
        setSchedule(data);
        setMessages([
          ...messages,
          {
            role: 'assistant',
            content: 'I\'ve generated an optimized schedule for you! Check it out below.',
          },
        ]);
      }
    } catch (error) {
      console.error('Error generating schedule:', error);
      setMessages([
        ...messages,
        {
          role: 'assistant',
          content: 'Sorry, I had trouble generating a schedule. Please try again.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const suggestedQuestions = [
    "I love coding and solving complex problems. What majors should I consider?",
    "I want to help people and work in healthcare. What are my options?",
    "I'm interested in business and entrepreneurship. What should I study?",
    "I enjoy writing, reading, and creative work. What majors fit me?",
  ];

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>🎓 BYU Major Advisor</h1>
          <p>AI-powered guidance to help you discover the perfect major and optimize your academic path</p>
        </div>
      </header>

      <main className="main-content">
        <div className="chat-container">
          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <h2>Welcome to BYU Major Advisor! 👋</h2>
                <p>
                  I'm here to help you explore majors at BYU. Tell me about your interests, 
                  passions, and career goals, and I'll recommend majors that match your profile. 
                  I can also create an optimized first-year schedule that keeps multiple academic 
                  paths open!
                </p>
                <div className="suggested-questions">
                  <p style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>Try asking:</p>
                  {suggestedQuestions.map((question, idx) => (
                    <div
                      key={idx}
                      className="suggested-question"
                      onClick={() => handleSendMessage(question)}
                    >
                      {question}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <>
                {messages.map((msg, idx) => (
                  <ChatMessage key={idx} message={msg.content} role={msg.role} />
                ))}
                {isLoading && (
                  <div className="message assistant">
                    <div className="message-content">
                      <div className="loading"></div>
                    </div>
                  </div>
                )}
              </>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-container">
            <form className="chat-input-form" onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }}>
              <input
                type="text"
                className="chat-input"
                placeholder="Tell me about your interests..."
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isLoading}
              />
              <button
                type="submit"
                className="send-button"
                disabled={isLoading || !inputMessage.trim()}
              >
                {isLoading ? <span className="loading"></span> : 'Send'}
              </button>
            </form>
          </div>
        </div>

        {majorDetails.length > 0 && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '2rem', marginBottom: '1rem' }}>
              <h2 style={{ color: 'var(--byu-blue)' }}>Recommended Majors</h2>
              <button
                className="send-button"
                onClick={handleGenerateSchedule}
                disabled={isLoading}
              >
                Generate Schedule
              </button>
            </div>
            <div className="major-recommendations">
              {majorDetails.map((major, idx) => (
                <MajorCard key={idx} major={major} />
              ))}
            </div>
          </div>
        )}

        {schedule && (
          <ScheduleDisplay
            schedule={schedule.schedule}
            reasoning={schedule.reasoning}
            majorsConsidered={schedule.majors_considered}
            semester={schedule.semester}
          />
        )}
      </main>
    </div>
  );
}

export default App;
