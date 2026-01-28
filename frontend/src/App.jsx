import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Sidebar from "./components/Sidebar.jsx";
import Navbar from "./components/Navbar.jsx";
import Welcome from "./components/Welcome.jsx";
import ChatMessage from "./components/ChatMessage.jsx";
import ChatInput from "./components/ChatInput.jsx";
import CategoriesView from "./components/CategoriesView.jsx";
import { searchAndAnswer } from "./services/api.js";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [showCategories, setShowCategories] = useState(false);
  const [categoriesViewMode, setCategoriesViewMode] = useState("categories");
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleNewChat = () => {
    setMessages([]);
  };

  const handleSendMessage = async (content) => {
    // Add user message
    const userMessage = { role: "user", content };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await searchAndAnswer(content);
      const assistantMessage = {
        role: "assistant",
        content: response.answer,
        sources: response.sources,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        role: "assistant",
        content: `⚠️ Error: ${error.message || "Failed to get response. Please try again."}`,
        sources: "",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    handleSendMessage(suggestion);
  };

  const handleServiceClick = (service) => {
    // When a service is clicked, send a message asking about it
    const query = `Tell me about ${service.service_name}`;
    handleSendMessage(query);
    setShowCategories(false);
  };

  const handleToggleCategories = () => {
    setShowCategories(!showCategories);
    if (!showCategories) {
      setMessages([]);
    }
  };

  const handleToggleCategoriesMode = () => {
    setCategoriesViewMode((prev) =>
      prev === "categories" ? "subcategories" : "categories",
    );
  };

  return (
    <div className="app">
      <Sidebar
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        onNewChat={handleNewChat}
      />

      <main className={`main-content ${sidebarOpen ? "" : "sidebar-closed"}`}>
        <Navbar
          sidebarOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          onToggleCategories={handleToggleCategories}
          showingCategories={showCategories}
          categoriesViewMode={categoriesViewMode}
          onToggleCategoriesMode={handleToggleCategoriesMode}
        />

        <div className="chat-container">
          {showCategories ? (
            <CategoriesView
              onServiceClick={handleServiceClick}
              viewMode={categoriesViewMode}
            />
          ) : messages.length === 0 ? (
            <Welcome onSuggestionClick={handleSuggestionClick} />
          ) : (
            <div className="messages-container">
              <AnimatePresence>
                {messages.map((message, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ duration: 0.3 }}
                  >
                    <ChatMessage message={message} />
                  </motion.div>
                ))}
              </AnimatePresence>
              {isLoading && (
                <motion.div
                  className="message assistant"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div className="message-avatar">
                    <img
                      src="/logo.jpeg"
                      alt="VIDHI.AI"
                      className="avatar-logo"
                    />
                  </div>
                  <div className="message-content">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </motion.div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        <ChatInput onSend={handleSendMessage} disabled={isLoading} />
      </main>
    </div>
  );
}

export default App;
