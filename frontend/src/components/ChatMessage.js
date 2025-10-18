import React from 'react';

const ChatMessage = ({ message, role }) => {
  return (
    <div className={`message ${role}`}>
      <div className="message-content">
        {message}
      </div>
    </div>
  );
};

export default ChatMessage;
