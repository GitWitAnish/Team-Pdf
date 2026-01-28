import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { ChevronDown, ChevronUp, FileText, Scale } from "lucide-react";
import "./ChatMessage.css";

function ChatMessage({ message }) {
  const [sourcesExpanded, setSourcesExpanded] = useState(false);
  const isUser = message.role === "user";

  return (
    <div className={`message ${isUser ? "user" : "assistant"}`}>
      <div className="message-avatar">{isUser ? "Y" : <Scale size={18} />}</div>

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
          {message.content}
        </ReactMarkdown>

        {!isUser && message.sources && (
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
                <ReactMarkdown>{message.sources}</ReactMarkdown>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatMessage;
