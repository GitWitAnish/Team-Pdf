import React, { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
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
    <motion.div
      className="chat-input-container"
      initial={{ y: 50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.4, delay: 0.2 }}
    >
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <motion.div
          className="chat-input-wrapper"
          whileFocus={{ scale: 1.01 }}
          transition={{ duration: 0.2 }}
        >
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={isListening ? "Listening..." : "Message VIDHI.AI"}
            disabled={disabled}
            rows={1}
            className={`chat-textarea ${isListening ? "listening" : ""}`}
          />
          {isSupported && (
            <motion.button
              type="button"
              className={`voice-button ${isListening ? "recording" : ""}`}
              onClick={handleVoiceClick}
              disabled={disabled}
              aria-label={
                isListening ? "Stop recording" : "Start voice recording"
              }
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              animate={isListening ? { scale: [1, 1.2, 1] } : { scale: 1 }}
              transition={{
                scale: { repeat: isListening ? Infinity : 0, duration: 1 },
              }}
            >
              {isListening ? <Square size={18} /> : <Mic size={18} />}
            </motion.button>
          )}
          <motion.button
            type="submit"
            className="send-button"
            disabled={!input.trim() || disabled}
            whileHover={{ scale: 1.1, rotate: 5 }}
            whileTap={{ scale: 0.9 }}
            transition={{ duration: 0.2 }}
            style={{
              background: input.trim()
                ? "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)"
                : "linear-gradient(135deg, #374151 0%, #1f2937 100%)",
              color: input.trim() ? "#ffffff" : "#9ca3af",
            }}
          >
            <ArrowUp size={20} />
          </motion.button>
        </motion.div>
      </form>
      <motion.p
        className="input-disclaimer"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        This AI can make mistakes. This is information not advice, try
        cousulting real lawyer if needed.
      </motion.p>
    </motion.div>
  );
}

export default ChatInput;
