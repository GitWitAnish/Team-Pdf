import React, { useState, useRef, useEffect } from "react";
import { ArrowUp } from "lucide-react";
import "./ChatInput.css";

function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState("");
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "24px";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [input]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput("");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-input-container">
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <div className="chat-input-wrapper">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message Nepal Legal AI..."
            disabled={disabled}
            rows={1}
            className="chat-textarea"
          />
          <button
            type="submit"
            className="send-button"
            disabled={!input.trim() || disabled}
          >
            <ArrowUp size={20} />
          </button>
        </div>
      </form>
      <p className="input-disclaimer">
        This AI can make mistakes. This is information not advice, try cousulting real lawyer if needed.
      </p>
    </div>
  );
}

export default ChatInput;
