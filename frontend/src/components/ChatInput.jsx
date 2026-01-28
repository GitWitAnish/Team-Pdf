import React, { useState, useRef, useEffect } from "react";
import { ArrowUp, Mic, Square } from "lucide-react";
import { useSpeechToText } from "../hooks/useSpeechToText";
import "./ChatInput.css";

function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState("");
  const textareaRef = useRef(null);

  const {
    isListening,
    transcript,
    interimTranscript,
    startListening,
    stopListening,
    resetTranscript,
    isSupported,
  } = useSpeechToText();

  useEffect(() => {
    if (transcript) {
      setInput(transcript + (interimTranscript ? " " + interimTranscript : ""));
    }
  }, [transcript, interimTranscript]);

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
      resetTranscript();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleVoiceClick = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
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
            placeholder={
              isListening ? "Listening..." : "Message Nepal Legal AI..."
            }
            disabled={disabled}
            rows={1}
            className={`chat-textarea ${isListening ? "listening" : ""}`}
          />
          {isSupported && (
            <button
              type="button"
              className={`voice-button ${isListening ? "recording" : ""}`}
              onClick={handleVoiceClick}
              disabled={disabled}
              aria-label={
                isListening ? "Stop recording" : "Start voice recording"
              }
            >
              {isListening ? <Square size={18} /> : <Mic size={18} />}
            </button>
          )}
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
