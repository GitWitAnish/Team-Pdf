import React from "react";
import { Plus, PanelLeftClose, PanelLeft, LogOut } from "lucide-react";
import logo from "/logo.jpeg";
import "./Sidebar.css";

function Sidebar({ isOpen, onToggle, onNewChat }) {
  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && <div className="sidebar-overlay" onClick={onToggle} />}

      <aside className={`sidebar ${isOpen ? "open" : "closed"}`}>
        <div className="sidebar-top">
          <div className="sidebar-logo-section">
            <img src={logo} alt="VIDHI.AI" className="sidebar-logo" />
            {/* <span className="sidebar-logo-text">VIDHI.AI</span> */}
          </div>
          <button
            className="sidebar-close-btn"
            onClick={onToggle}
            aria-label="Close sidebar"
          >
            <PanelLeftClose size={20} />
          </button>
        </div>

        <div className="sidebar-actions">
          <button className="new-chat-btn" onClick={onNewChat}>
            <Plus size={20} />
            <span>New chat</span>
          </button>
        </div>

        <div className="sidebar-content">
          <div className="chat-history-section">
            <span className="history-label">Today</span>
            {/* Chat history items would go here */}
          </div>
        </div>

        <div className="sidebar-bottom">
          <div className="sidebar-divider" />
          <div className="user-section">
            <div className="user-avatar">A</div>
            <span className="user-name">Anish</span>
            <button className="logout-btn" aria-label="Logout">
              <LogOut size={18} />
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}

export default Sidebar;
