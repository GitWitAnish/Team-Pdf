import React from "react";
import { Scale, FileText, Building2, Briefcase, Shield } from "lucide-react";
import logo from "/logo.jpeg";
import "./Welcome.css";

const suggestions = [
  {
    icon: <FileText size={20} />,
    title: "Fundamental Rights",
    text: "What are the fundamental rights in Nepal's constitution?",
    query:
      "What are the fundamental rights guaranteed by the Constitution of Nepal?",
  },
  {
    icon: <Building2 size={20} />,
    title: "Citizenship Laws",
    text: "How is citizenship acquired in Nepal?",
    query: "How can someone acquire Nepali citizenship?",
  },
  {
    icon: <Briefcase size={20} />,
    title: "Civil Service",
    text: "What are employee rights in civil service?",
    query:
      "What are the rights and benefits of civil service employees in Nepal?",
  },
  {
    icon: <Shield size={20} />,
    title: "Privacy Laws",
    text: "What are privacy laws in Nepal?",
    query: "What does Nepal's Individual Privacy Act protect?",
  },
];

function Welcome({ onSuggestionClick }) {
  return (
    <div className="welcome-container">
      <div className="welcome-content">
        <div className="welcome-logo-wrapper">
          <img src={logo} alt="Nyaya.exe" className="welcome-logo" />
        </div>

        <h1 className="welcome-title">Nyaya.exe</h1>
        <p className="welcome-subtitle">
          Load embedding model and FAISS store.
        </p>

        <div className="suggestions-grid">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              className="suggestion-card"
              onClick={() => onSuggestionClick(suggestion.query)}
            >
              <div className="suggestion-content">
                <span className="suggestion-title">{suggestion.title}</span>
                <span className="suggestion-text">{suggestion.text}</span>
              </div>
              <span className="suggestion-icon">{suggestion.icon}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Welcome;
