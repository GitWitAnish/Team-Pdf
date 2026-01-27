import React from "react";
import { PanelLeft, Share, MoreHorizontal } from "lucide-react";
import "./Navbar.css";

function Navbar({ sidebarOpen, onToggleSidebar }) {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        {!sidebarOpen && (
          <button
            className="navbar-btn"
            onClick={onToggleSidebar}
            aria-label="Open sidebar"
          >
            <PanelLeft size={20} />
          </button>
        )}
        <span className="navbar-title">Nyaya.exe</span>
      </div>
      <div className="navbar-right">
        <button className="navbar-btn" aria-label="Share">
          <Share size={18} />
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
