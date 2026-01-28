import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import {
  ChevronDown,
  ChevronUp,
  FileText,
  Scale,
  Volume2,
  VolumeX,
} from "lucide-react";
import { useTextToSpeech } from "../hooks/useTextToSpeech";
import "./ChatMessage.css";

function ChatMessage({ message }) {
  const [sourcesExpanded, setSourcesExpanded] = useState(false);
  const { speak, stop, isSpeaking } = useTextToSpeech();
  const isUser = message.role === "user";

  const handleSpeak = () => {
    if (isSpeaking) {
      stop();
    } else {
      // Remove markdown formatting for cleaner speech
      const plainText = message.content
        .replace(/\*\*/g, "")
        .replace(/\*/g, "")
        .replace(/#{1,6}\s/g, "")
        .replace(/\[([^\]]+)\]\([^\)]+\)/g, "$1")
        .replace(/`/g, "");

      speak(plainText);
    }
  };

  return (
    <div className={`message ${isUser ? "user" : "assistant"}`}>
      <div className="message-avatar">{isUser ? "A" : <Scale size={18} />}</div>

      <div className="message-content">
        <ReactMarkdown
          components={{
            p: ({ children }) => <p>{children}</p>,
            code: ({ inline, children, ...props }) => {
              if (inline) {
                return <code {...props}>{children}</code>;
              }
              return (
                <pre>
                  <code {...props}>{children}</code>
                </pre>
              );
            },
            blockquote: ({ children }) => <blockquote>{children}</blockquote>,
          }}
        >
          {message.content || ""}
        </ReactMarkdown>

        {!isUser && (
          <div className="message-actions">
            <button
              className={`speak-button ${isSpeaking ? "speaking" : ""}`}
              onClick={handleSpeak}
              title={isSpeaking ? "Stop speaking" : "Read aloud"}
            >
              {isSpeaking ? <VolumeX size={18} /> : <Volume2 size={18} />}
            </button>

            {message.sources && (
              <div className="sources-section">
                <button
                  className="sources-toggle"
                  onClick={() => setSourcesExpanded(!sourcesExpanded)}
                >
                  <FileText size={16} />
                  <span>Sources</span>
                  {sourcesExpanded ? (
                    <ChevronUp size={16} />
                  ) : (
                    <ChevronDown size={16} />
                  )}
                </button>

                {sourcesExpanded && (
                  <div className="sources-content">
                    <ReactMarkdown>{message.sources || ""}</ReactMarkdown>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatMessage;
